# Generated by Django 5.0 on 2024-01-01 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('msestocks', '0002_rename_precent_change_stock_precentchange'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='precentchange',
            new_name='precent_change',
        ),
    ]