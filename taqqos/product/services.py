import requests
from django.db import transaction
from django.core.files.base import ContentFile
from django.contrib.postgres.search import TrigramSimilarity

from taqqos.celery import app
from taqqos.document.models import File
from taqqos.document.services import create_thumbnail_image
from taqqos.product.models import ProductPrice, Product


@app.task
def create_product_price(data: dict, *args, **kwargs) -> None:
    with transaction.atomic():
        name = data.pop("name")
        website = data.pop("website")
        photo = data.pop("photo")
        product_price, _ = ProductPrice.objects.update_or_create(
            name=name, website=website, defaults=dict(**data)
        )
        if photo:
            product_price.image_url = photo
            product_price.save()
            try:
                product_price.photo = None
                # r = requests.get(photo, verify=False)
                # if r.status_code == 200:
                #     filename = photo.split('/')[-1]
                #     if website == "Mediapark":
                #         filename = filename.split("&")[0]
                #     file = File(
                #         name=filename,
                #         file_type=File.IMAGE
                #     )
                #     file.file.save(filename, ContentFile(r.content))
                #     file.save()
                #     create_thumbnail_image(file)
                #     product_price.photo = file
                #     product_price.save()
            except Exception as e:
                print(e)
        # products = Product.objects.filter(name_ru__trigram_strict_word_similar=name)
        products = Product.objects.all()

        matched_products = []
        for product in products:
            product_name_words = product.short_name.lower().split(" ")
            every_word_in_name = True
            for word in product_name_words:
                if word not in name.lower():
                    every_word_in_name = False
            if every_word_in_name:
                matched_products.append(product)
                print(product.short_name)

        if matched_products:
            print("There is some products man")
            product_price.products.add(*matched_products)
            product_price.save()
        else:
            print("No any products bro, but saved anyway")
            product_price.save()
