from django.db import models
from datetime import datetime


# Get and store stock data

class Stock(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    current_open_price = models.FloatField()
    current_close_price = models.FloatField()
    percent_change = models.FloatField()
    current_volume = models.IntegerField()
    current_turnover = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

class HistoricalStockData(models.Model):
    stock = models.ForeignKey(Stock, related_name='historical_data', on_delete=models.CASCADE)
    open_price = models.FloatField()
    close_price = models.FloatField()
    percent_change = models.FloatField()
    volume = models.IntegerField()
    turnover = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.timestamp}"