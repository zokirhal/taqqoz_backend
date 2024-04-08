from taqqos.celery import app
from taqqos.product.models import Product, ProductPrice


@app.task
def match_products_price():
    for product in Product.objects.all():
        if product.short_name:
            product.product_prices.clear()
            product_prices = ProductPrice.objects.filter(
                name__icontains=product.short_name
            )
            if product_prices:
                print(product.short_name)
                print(product_prices.values_list("name"))
                product.product_prices.add(*product_prices)
            product.save()
