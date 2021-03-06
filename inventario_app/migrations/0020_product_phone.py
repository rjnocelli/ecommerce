# Generated by Django 3.1.3 on 2020-11-16 18:26

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0019_auto_20201116_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]
