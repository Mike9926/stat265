# msestocks/urls.py
from django.urls import path
from . views import stock_list, stock_detail


app_name = 'msestocks'

urlpatterns = [
    path('', stock_list, name='index'),  # This is for the homepage
    path('stocks/<int:id>/', stock_detail, name='stock-detail'),
]
