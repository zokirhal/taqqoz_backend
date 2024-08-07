from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .product.views.product import OptionAutocomplete

from taqqos.core.swagger import urlpatterns as doc_urls
urlpatterns = doc_urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('option-autocomplete/', OptionAutocomplete.as_view(), name='option-autocomplete'),
    path("select2/", include("django_select2.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('<version>/account/', include("taqqos.account.urls")),
    path('<version>/document/', include("taqqos.document.urls")),
    path('<version>/', include("taqqos.product.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
