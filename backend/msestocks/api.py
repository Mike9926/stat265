from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Stock
from django.db.models import Max


@api_view(['GET'])
def market_summary(request):
    """Return a market summary built from Stock rows.

    Fields:
    - index: static label 'MSE'
    - value: approximate index value (sum of close prices of top N by volume)
    - change_percent: weighted average percent_change
    - gainers: top 5 stocks by percent_change desc
    - losers: top 5 stocks by percent_change asc
    """
    qs = Stock.objects.all()

    # approximate index: sum of top 10 close prices (simple heuristic)
    top_by_volume = list(qs.order_by('-current_volume')[:10])
    index_value = round(sum([s.current_close_price for s in top_by_volume]) if top_by_volume else 0, 2)

    # weighted avg change
    if top_by_volume:
        weights = [s.current_volume or 1 for s in top_by_volume]
        weighted = sum((s.percent_change or 0) * w for s, w in zip(top_by_volume, weights)) / sum(weights)
        change_pct = round(weighted, 2)
    else:
        change_pct = 0.0

    gainers = list(qs.filter(percent_change__isnull=False).order_by('-percent_change')[:5].values('symbol', 'percent_change', 'current_close_price'))
    losers = list(qs.filter(percent_change__isnull=False).order_by('percent_change')[:5].values('symbol', 'percent_change', 'current_close_price'))

    data = {
        'index': 'MSE',
        'value': index_value,
        'change_percent': change_pct,
        'gainers': gainers,
        'losers': losers,
    }

    return Response(data)


@api_view(['GET'])
def stocks_list(request):
    """Return a compact list of stocks for market pages."""
    qs = Stock.objects.all().order_by('-current_volume')
    data = list(qs.values('id','symbol','current_close_price','percent_change','current_volume')[:200])
    return Response(data)


@api_view(['GET'])
def stock_detail_api(request, id):
    s = Stock.objects.filter(id=id).values('id','symbol','current_close_price','current_open_price','percent_change','current_volume','current_turnover').first()
    if not s:
        return Response({'detail':'Not found'}, status=404)
    # attach simple historical series (timestamps and close)
    series = list(s and Stock.objects.get(id=id).historical_data.all().order_by('timestamp').values('timestamp','close_price')[:500])
    s['historical'] = series
    return Response(s)
