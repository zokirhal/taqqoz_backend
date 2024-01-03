# Generated by Django 4.2.7 on 2024-01-03 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_category_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='text_value',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='toggle_value',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='options',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_attributes', to='product.option', verbose_name='параметр'),
        ),
    ]
