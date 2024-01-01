from django.contrib import admin
from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'current_open_price', 'current_close_price', 'percent_change', 'current_volume', 'current_turnover', 'last_updated')
    list_filter = ('last_updated',)
    
admin.site.register(Stock, StockAdmin)
