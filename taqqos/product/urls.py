from django.urls import path, include
from rest_framework.routers import DefaultRouter

from taqqos.product.views import category, brand, product, review, favorite, sliders

router = DefaultRouter()
router.register('review', review.ReviewViewSet, 'review')
router.register('favorite', favorite.FavouriteView, 'favorite')


urlpatterns = [
    path("brand/", brand.BrandView.as_view(), name="brand"),
    path("category/", category.CategoryView.as_view({"get": "list", }), name="category"),
    path("category/<int:pk>/", category.CategoryView.as_view({"get": "retrieve", }), name="category"),
    path("product/", product.ProductViewSet.as_view({"get": "list", }), name="product"),
    path("product/<int:pk>/", product.ProductViewSet.as_view({"get": "retrieve", }), name="product-read"),
    path("product/detail/<str:slug>/", product.ProductDetailView.as_view(), name="product-detail"),
    path("product/price/", product.ProductPriceViewSet.as_view({"get": "list", }), name="product-price"),
    path("product/price/<int:pk>/", product.ProductPriceViewSet.as_view({"get": "retrieve", }), name="product-price"),
    path("product/price/create/", product.ProductPriceCreateView.as_view(), name="product-price-create"),
    path("slider/", sliders.SliderView.as_view(), name="slider"),
    path("seller/", sliders.SellerView.as_view(), name="seller"),
    path('', include(router.urls))
]
