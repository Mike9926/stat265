from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
import requests
from bs4 import BeautifulSoup
from .models import Stock, HistoricalStockData
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import fields


def update_stock_data():
    URL = 'https://mse.co.mw/market/mainboard'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    table_body = soup.find('tbody')

    for row in table_body.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) >= 6:
            symbol = cells[0].text.strip()
            open_price = float(cells[1].text.replace(',', '').strip())
            close_price = float(cells[2].text.replace(',', '').strip())
            percent_change = round(((close_price - open_price) / open_price) * 100, 2) if open_price != 0 else 0.0
            volume_str = cells[4].text.strip().replace(',', '')
            volume = float(volume_str) if volume_str else 0.0
            turnover_str = cells[5].text.strip().replace(',', '') if len(cells) > 5 else ''
            turnover = float(turnover_str) if turnover_str else 0.0

            stock, created = Stock.objects.get_or_create(symbol=symbol)
            HistoricalStockData.objects.get_or_create(
                stock=stock,
                timestamp__date=timezone.now().date(),
                defaults={
                    'open_price': open_price,
                    'close_price': close_price,
                    'percent_change': percent_change,
                    'volume': volume,
                    'turnover': turnover,
                }
            )

    tfoot = soup.find('tfoot')
    if tfoot:
        timestamp_text = tfoot.find('i')
        if timestamp_text:
            timestamp_str = timestamp_text.text.strip().replace('Stats as at ', '')
            timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M%p')
            Stock.objects.update(last_updated=timestamp)


def stock_list(request):
    update_stock_data()

    # Fetch stock data from the database
    stocks = Stock.objects.all()
    popular_stocks = stocks[:5]  # Adjust as necessary to get the popular stocks
    actives_stocks = stocks[:4]  # Placeholder, replace with actual logic
    gainers_stocks = stocks.filter(percent_change__gt=0)[:4]
    losers_stocks = stocks.filter(percent_change__lt=0)[:4]
    watchlist_stocks = stocks[:4]  # Placeholder, replace with actual logic

    context = {
        'stocks': stocks,
        'popular_stocks': popular_stocks,
        'actives_stocks': actives_stocks,
        'gainers_stocks': gainers_stocks,
        'losers_stocks': losers_stocks,
        'watchlist_stocks': watchlist_stocks,
    }

    return render(request, 'msestocks/index.html', context)


def stock_detail(request, id):
    stock = get_object_or_404(Stock, id=id)
    historical_data = serialize('json', stock.historical_data.all(), fields=('timestamp', 'close_price'))

    context = {
        'stock': stock,
        'historical_data': historical_data,
    }

    return render(request, 'msestocks/stock_detail.html', context)
