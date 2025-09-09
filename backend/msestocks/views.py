from django.shortcuts import render, get_object_or_404
from django.core.serializers import serialize
import requests
from bs4 import BeautifulSoup
from .models import Stock, HistoricalStockData
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import fields
from django.views.decorators.http import require_GET


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
    # Only trigger a live scrape when explicitly requested to avoid
    # making an external request on every page load.
    if request.GET.get('update') == '1':
        update_stock_data()

    # Search
    q = request.GET.get('q', '').strip()
    stocks_qs = Stock.objects.all().order_by('-current_volume', 'symbol')
    if q:
        stocks_qs = stocks_qs.filter(symbol__icontains=q)

    # simple selections for the sidebar / highlights
    popular_stocks = Stock.objects.all().order_by('-current_volume')[:5]
    actives_stocks = Stock.objects.all().order_by('-current_volume')[:4]
    gainers_stocks = Stock.objects.filter(percent_change__gt=0).order_by('-percent_change')[:4]
    losers_stocks = Stock.objects.filter(percent_change__lt=0).order_by('percent_change')[:4]
    watchlist_stocks = Stock.objects.all().order_by('-percent_change')[:4]

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(stocks_qs, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'popular_stocks': popular_stocks,
        'actives_stocks': actives_stocks,
        'gainers_stocks': gainers_stocks,
        'losers_stocks': losers_stocks,
        'watchlist_stocks': watchlist_stocks,
        'q': q,
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


@require_GET
def stock_data(request, id):
    """Return historical OHLCV data for a stock as JSON.

    We don't assume intraday granularity exists; high/low are approximated
    when only open/close are available.
    """
    stock = get_object_or_404(Stock, id=id)
    qs = stock.historical_data.all().order_by('timestamp')

    series = []
    for row in qs:
        open_p = getattr(row, 'open_price', None) or 0.0
        close_p = getattr(row, 'close_price', None) or 0.0
        high_p = max(open_p, close_p)
        low_p = min(open_p, close_p)
        series.append({
            'time': row.timestamp.isoformat(),
            'open': open_p,
            'high': high_p,
            'low': low_p,
            'close': close_p,
            'volume': getattr(row, 'volume', 0),
        })

    return JsonResponse(series, safe=False)
