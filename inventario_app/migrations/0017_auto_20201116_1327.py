# Generated by Django 3.1.3 on 2020-11-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0016_auto_20201116_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=400, verbose_name='descripcion'),
        ),
    ]
