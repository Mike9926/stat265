# msestocks/urls.py
from django.urls import path
from .views import stock_list

app_name = 'msestocks'

urlpatterns = [
    path('', stock_list, name='index'),  # This is for the homepage
    # Add more patterns as needed
]
