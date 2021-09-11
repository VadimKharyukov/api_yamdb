from rest_framework.routers import SimpleRouter

from django.urls import include, path

from api.views import TitleViewSet, CategoryViewSet, GenreViewSet

router = SimpleRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
