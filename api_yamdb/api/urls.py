from django.urls import include, path
from rest_framework import routers

from .views import *
#
# router = routers.DefaultRouter()
# router.register(r'users', CustomUserViewSet)


urlpatterns = [
    # path('v1/', include(router.urls)),
    path('v1/auth/signup/', singup),
    path('v1/auth/token/', token),

]

