# Generated by Django 3.1.3 on 2020-12-16 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0031_product_sold_by_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold_by_weight',
            field=models.BooleanField(default=False, verbose_name='Producto Vendido x Peso'),
        ),
    ]