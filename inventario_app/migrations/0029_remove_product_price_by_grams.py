# Generated by Django 3.1.3 on 2020-12-15 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0028_product_price_by_grams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_by_grams',
        ),
    ]
