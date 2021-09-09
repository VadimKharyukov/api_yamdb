from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import CustomUser
from .serializers import (
    SingupSerializer,
    # CustomUserSerializer,
    TokenSerializer
)


@api_view(['POST'])
def singup(request):
    serializer = SingupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    if username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user, create = CustomUser.objects.get_or_create(email=email,
                                                    username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Вам отправлен код авторизации',
              f'Ваш код {confirmation_code}',
              settings.DEFAULT_FROM_EMAIL, [email])
    return Response({'email': email, 'username': username})


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(CustomUser, username=username)
    token = AccessToken.for_user(user)
    if default_token_generator.check_token(user, confirmation_code):
        return Response('Ваш токен:',
                        f'{token}')
    return Response(status=status.HTTP_400_BAD_REQUEST)

#
# class CustomUserViewSet(viewsets.ModelViewSet):
#     serializer_class = AdminSerializer
#     queryset = CustomUser.objects.all()
#     permission_classes = (IsAdmin, )
#     search_fields = ('username',)
