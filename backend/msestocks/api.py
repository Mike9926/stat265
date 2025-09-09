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
