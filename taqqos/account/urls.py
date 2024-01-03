from django.urls import path, include

# Django Rest Framework
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

# Project
from taqqos.account.views.auth import PhoneAuthView
from taqqos.account.views.user import UserView

router = DefaultRouter()
router.register('auth', PhoneAuthView, 'auth')
# router.register('register', RegisterView, 'register')
router.register('user', UserView, 'user')

urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('', include(router.urls))
]
