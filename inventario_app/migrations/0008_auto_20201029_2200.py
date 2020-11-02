# Generated by Django 3.0.3 on 2020-10-29 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0007_order_costumer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='costumer',
            new_name='customer_email',
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
