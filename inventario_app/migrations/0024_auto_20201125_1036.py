# Generated by Django 3.1.3 on 2020-11-25 10:36

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0023_auto_20201125_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='chocolate.jpg', force_format='JPEG', keep_meta=True, null=True, quality=100, size=[100, 100], upload_to='', verbose_name='imagen'),
        ),
    ]
