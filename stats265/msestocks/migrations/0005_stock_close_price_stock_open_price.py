# Generated by Django 5.0 on 2024-01-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msestocks', '0004_rename_precent_change_stock_percent_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='close_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='stock',
            name='open_price',
            field=models.FloatField(default=0.0),
        ),
    ]
