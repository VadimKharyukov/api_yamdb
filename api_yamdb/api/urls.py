from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
                ReviewViewSet)
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
    )
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/'
    r'(?P<comment_id>\d+)', CommentViewSet
    )
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
]
