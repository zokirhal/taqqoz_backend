# Generated by Django 4.2.7 on 2023-11-24 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='categorytranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'категория Translation'},
        ),
    ]
