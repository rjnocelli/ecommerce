# Generated by Django 3.1.5 on 2021-05-26 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0037_auto_20210523_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_100g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='precio por 100g'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_200g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='precio por 200g'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_300g',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='precio por 300g'),
        ),
    ]
