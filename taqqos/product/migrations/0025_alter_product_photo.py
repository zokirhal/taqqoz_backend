# Generated by Django 4.2.7 on 2024-04-22 03:54

from django.db import migrations, models
import taqqos.document.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_productattribute_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=taqqos.document.models.upload_name, verbose_name='файл'),
        ),
    ]