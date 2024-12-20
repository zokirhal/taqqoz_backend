# Generated by Django 4.2.7 on 2023-12-12 11:37

from django.db import migrations, models
import taqqos.document.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('file', models.FileField(upload_to=taqqos.document.models.upload_name, verbose_name='файл')),
                ('file_type', models.CharField(blank=True, choices=[('video', 'video'), ('document', 'document'), ('image', 'image')], max_length=30, null=True, verbose_name='тип файла')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to=taqqos.document.models.upload_name)),
            ],
            options={
                'verbose_name': 'файл',
                'verbose_name_plural': 'файлы',
            },
        ),
    ]
