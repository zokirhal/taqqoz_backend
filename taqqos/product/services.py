import requests
from django.core.files.base import ContentFile
from django.db import transaction
from django.contrib.postgres.search import TrigramStrictWordSimilarity, TrigramWordDistance
from django.db.models import Q

from taqqos.celery import app
from taqqos.document.models import File
from taqqos.document.services import create_thumbnail_image
from taqqos.product.models import ProductPrice, Product


@app.task
def create_product_price(
        data: dict,
        *args, **kwargs
) -> None:
    with transaction.atomic():
        name = data.pop("name")
        website = data.pop("website")
        photo = data.pop("photo")
        product_price, _ = ProductPrice.objects.update_or_create(
            name=name,
            website=website,
            defaults=dict(
                **data
            )
        )
        if photo:
            r = requests.get(photo)
            if r.status_code == 200:
                filename = photo.split('/')[-1]
                if website == "Mediapark":
                    filename = filename.split("&")[0]
                file = File(
                    name=filename,
                    file_type=File.IMAGE
                )
                file.file.save(filename, ContentFile(r.content))
                file.save()
                create_thumbnail_image(file)
                product_price.photo = file
                product_price.save()
        products = Product.objects.filter(name_ru__trigram_strict_word_similar=name)
        if products:
            product_price.products.add(*products)
            product_price.save()


def match_product_price():
    for product in Product.objects.all():
        product.product_prices.clear()
        product_prices = ProductPrice.objects.filter(
            name__icontains=product.short_name
        )
        if product_prices:
            print(product.short_name)
            print(product_prices.values_list("name"))
            product.product_prices.add(*product_prices)
        product.save()
