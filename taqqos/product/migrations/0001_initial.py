# Generated by Django 4.2.7 on 2023-12-12 11:37

import ckeditor_uploader.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('document', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('code', models.CharField(max_length=64, verbose_name='код')),
                ('type', models.CharField(choices=[('text', 'text'), ('toggle', 'toggle'), ('option', 'option'), ('multi_option', 'multi_option')], max_length=64, verbose_name='тип')),
                ('is_required', models.BooleanField(verbose_name='требуется')),
                ('can_join', models.BooleanField(default=False, verbose_name='могу присоединиться')),
                ('order_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='порядковый номер')),
            ],
            options={
                'verbose_name': 'атрибут',
                'verbose_name_plural': 'атрибуты',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('order_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='порядковый номер')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.brand', verbose_name='родитель')),
            ],
            options={
                'verbose_name': 'бренд',
                'verbose_name_plural': 'бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('order_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='порядковый номер')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('brands', mptt.fields.TreeManyToManyField(related_name='categories', to='product.brand', verbose_name='бренды')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='родитель')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('code', models.CharField(max_length=64, verbose_name='код')),
                ('label', models.TextField(blank=True, null=True, verbose_name='метка')),
                ('order_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='порядковый номер')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='product.attribute', verbose_name='атрибут')),
            ],
            options={
                'verbose_name': 'параметр',
                'verbose_name_plural': 'параметры',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('is_popular', models.BooleanField(default=False, verbose_name='популярен')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('description_uz', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='описание uzb')),
                ('description_ru', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='описание rus')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.brand', verbose_name='бренд')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category', verbose_name='категория')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.file', verbose_name='фото')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('rate', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='ставка')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='product.product', verbose_name='продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='ReviewFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='document.file', verbose_name='файл')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_files', to='product.review', verbose_name='отзыв')),
            ],
            options={
                'verbose_name': 'отзыв файл',
                'verbose_name_plural': 'отзыв файлы',
            },
        ),
        migrations.CreateModel(
            name='ProductVideoReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='URL-адрес')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_reviews', to='product.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'видеообзор',
                'verbose_name_plural': 'видеообзоры',
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('name', models.CharField(max_length=512, verbose_name='название')),
                ('price_amount', models.CharField(max_length=256, verbose_name='сумма цены')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('feature', models.TextField(blank=True, null=True, verbose_name='характеристика')),
                ('has_credit', models.BooleanField(default=False, verbose_name='есть кредит')),
                ('credit_monthly_amount', models.CharField(blank=True, null=True, verbose_name='ежемесячная сумма кредита')),
                ('has_delivery', models.BooleanField(default=False, verbose_name='есть доставка')),
                ('delivery_info', models.TextField(blank=True, null=True, verbose_name='информация о доставке')),
                ('address', models.TextField(blank=True, null=True, verbose_name='адрес')),
                ('phone_number', models.CharField(blank=True, null=True, verbose_name='номер телефона')),
                ('website', models.CharField(max_length=256, verbose_name='Веб-сайт')),
                ('website_link', models.URLField(blank=True, null=True, verbose_name='ссылка на сайт')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_prices', to='product.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'цены на продукцию',
                'verbose_name_plural': 'цены на продукцию',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.file', verbose_name='фото')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'фото продукта',
                'verbose_name_plural': 'фотографии продукта',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(max_length=200, verbose_name='название uzb')),
                ('name_ru', models.CharField(max_length=200, verbose_name='название rus')),
                ('value', models.CharField(max_length=512, verbose_name='ценить')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='product.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'продукт характеристика',
                'verbose_name_plural': 'продукт характеристики',
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_value', models.CharField(blank=True, max_length=128, null=True, verbose_name='текстовое ценить')),
                ('toggle_value', models.BooleanField(blank=True, null=True, verbose_name='переключить ценить')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.attribute', verbose_name='атрибут')),
                ('options', models.ManyToManyField(blank=True, related_name='product_attributes', to='product.option', verbose_name='параметры')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='product.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'продукт атрибут',
                'verbose_name_plural': 'продукт атрибуты',
            },
        ),
        migrations.AddField(
            model_name='attribute',
            name='categories',
            field=mptt.fields.TreeManyToManyField(blank=True, related_name='attributes', to='product.category', verbose_name='категории'),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='product.product', verbose_name='продукт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Избранной',
                'verbose_name_plural': 'Избранное',
                'unique_together': {('user', 'product')},
            },
        ),
    ]
