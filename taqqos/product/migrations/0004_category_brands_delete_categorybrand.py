# Generated by Django 4.2.7 on 2023-12-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_description_ru_product_description_uz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='brands',
            field=models.ManyToManyField(related_name='categories', to='product.brand'),
        ),
        migrations.DeleteModel(
            name='CategoryBrand',
        ),
    ]
