# Generated by Django 4.2.7 on 2023-12-11 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sms_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
