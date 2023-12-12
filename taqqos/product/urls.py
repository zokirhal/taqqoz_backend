from django.urls import path, include
from rest_framework.routers import DefaultRouter

from taqqos.product.views import category, brand, product, review, favorite

router = DefaultRouter()
router.register('review', review.ReviewViewSet, 'review')
router.register('favorite', favorite.FavouriteView, 'favorite')


urlpatterns = [
    path("brand/", brand.BrandView.as_view(), name="brand"),
    path("category/", category.CategoryView.as_view({"get": "list", }), name="category"),
    path("category/<int:pk>/", category.CategoryView.as_view({"get": "retrieve", }), name="category"),
    path("product/", product.ProductViewSet.as_view({"get": "list", }), name="product"),
    path("product/<int:pk>/", product.ProductViewSet.as_view({"get": "retrieve", }), name="product"),
    path('', include(router.urls))
]
