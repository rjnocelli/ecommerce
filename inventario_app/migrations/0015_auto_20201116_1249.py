# Generated by Django 3.1.3 on 2020-11-16 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0014_auto_20201116_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='chocolate.jpg', null=True, upload_to='images', verbose_name='imagen'),
        ),
    ]
