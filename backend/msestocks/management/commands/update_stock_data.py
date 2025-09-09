from django.core.management.base import BaseCommand
from msestocks.views import update_stock_data

class Command(BaseCommand):
    help = 'Updates stock data'

    def handle(self, *args, **options):
        update_stock_data()

