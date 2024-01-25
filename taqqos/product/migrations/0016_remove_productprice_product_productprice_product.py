# Generated by Django 4.2.7 on 2024-01-23 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_alter_productprice_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productprice',
            name='product',
        ),
        migrations.AddField(
            model_name='productprice',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_prices', to='product.product', verbose_name='продукт'),
        ),
    ]
