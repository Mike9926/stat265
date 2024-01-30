from django.db import models
from django.utils import timezone



# Get and store stock data

class Stock(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    current_open_price = models.FloatField()
    current_close_price = models.FloatField()
    percent_change = models.FloatField()
    current_volume = models.IntegerField()
    current_turnover = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Set last_updated to current time in UTC when saving the object
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)
 
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
    
    def save(self, *args, **kwargs):
        # Update the stock fields with the latest data
        self.stock.current_open_price = self.open_price
        self.stock.current_close_price = self.close_price
        self.stock.percent_change = self.percent_change
        self.stock.current_volume = self.volume
        self.stock.current_turnover = self.turnover
        # Save the stock instance
        self.stock.save()
        # Call the super save method
        super().save(*args, **kwargs)