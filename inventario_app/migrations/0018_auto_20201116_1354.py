# Generated by Django 3.1.3 on 2020-11-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario_app', '0017_auto_20201116_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Categorias'),
        ),
    ]