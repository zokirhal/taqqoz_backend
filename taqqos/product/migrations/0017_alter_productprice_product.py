# Generated by Django 4.2.7 on 2024-01-23 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_remove_productprice_product_productprice_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productprice',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='product_prices', to='product.product', verbose_name='продукт'),
        ),
    ]