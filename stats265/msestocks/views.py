from django.shortcuts import render, get_object_or_404
import requests
from bs4 import BeautifulSoup
from .models import Stock, HistoricalStockData
from datetime import datetime
from django.utils import timezone

def update_stock_data():
    URL = 'https://mse.co.mw/market/mainboard'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_body = soup.find('tbody')

    for row in table_body.find_all('tr'):
        cells = row.find_all('td')

        # Check if there are at least 6 columns in the row
        if len(cells) >= 6:
            symbol = cells[0].text.strip()
            open_price = float(cells[1].text.replace(',', '').strip())
            close_price = float(cells[2].text.replace(',', '').strip())

            # Calculate percentage change and round to two decimal places
            percent_change = round(((close_price - open_price) / open_price) * 100, 2) if open_price != 0 else 0.0

            # Convert volume to float since it can have decimal points
            volume_str = cells[4].text.strip().replace(',', '')
            volume = float(volume_str) if volume_str else 0.0

            # Check if the index 5 exists before accessing
            turnover_str = cells[5].text.strip().replace(',', '') if len(cells) > 5 else ''
            turnover = float(turnover_str) if turnover_str else 0.0

            # Check if historical data with the same date and parameters exists
            stock = Stock.objects.get(symbol=symbol)
            historical_data, created = HistoricalStockData.objects.get_or_create(
                stock=stock,
                timestamp__date=timezone.now().date(),
                open_price=open_price,
                close_price=close_price,
                percent_change=percent_change,
                volume=volume,
                turnover=turnover,
            )
            # Save the historical data if it already exists
            if not created:
                historical_data.save()


    tfoot = soup.find('tfoot')
    if tfoot:
        timestamp_text = tfoot.find('i')
        if timestamp_text:
            timestamp_str = timestamp_text.text.strip().replace('Stats as at ', '')
            timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M%p')
            Stock.objects.update(last_updated=timestamp)

def stock_list(request):
    # Update stock data before rendering the template
    update_stock_data()

    # Fetch stock data from the database
    stocks = Stock.objects.all()
    return render(request, 'msestocks/index.html', {'stocks': stocks})

#stock detail view
def stock_detail(request, id):
    # Get the stock object or return a 404 error if not found
    stock = get_object_or_404(Stock, id=id)
    # Render the stock_detail.html template with the stock object as a context variable
    return render(request, 'msestocks/stock_detail.html', {'stock': stock})
     
    