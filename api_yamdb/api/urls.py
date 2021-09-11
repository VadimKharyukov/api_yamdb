from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import TitleViewSet, CategoryViewSet, GenreViewSet
from rest_framework import routers

from .views import *


router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
]
