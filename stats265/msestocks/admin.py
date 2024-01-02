from django.contrib import admin
from .models import Stock, HistoricalStockData


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'current_open_price', 'current_close_price', 'percent_change', 'current_volume', 'current_turnover', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('symbol',)
    date_hierarchy = 'last_updated'

@admin.register(HistoricalStockData)
class HistoricalStockDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'open_price', 'close_price', 'percent_change', 'volume', 'turnover', 'timestamp')
    list_filter = ('timestamp', 'stock__symbol')
    search_fields = ('stock__symbol',)
    date_hierarchy = 'timestamp'