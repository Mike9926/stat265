from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def market_summary(request):
    # Minimal sample response. Replace with real DB queries.
    data = {
        'index': 'MSE',
        'value': 85460.23,
        'change_percent': 0.85,
        'gainers': [
            {'symbol':'TNA','change':3.2},
            {'symbol':'NNL','change':2.1}
        ],
        'losers': [
            {'symbol':'ABC','change':-1.22},
            {'symbol':'XYZ','change':-0.87}
        ]
    }
    return Response(data)
