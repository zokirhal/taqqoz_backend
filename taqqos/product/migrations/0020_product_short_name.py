# Generated by Django 4.2.7 on 2024-02-24 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_remove_productprice_feature_productprice_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='название короткое'),
        ),
    ]
