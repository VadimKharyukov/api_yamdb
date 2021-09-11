from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import CustomUser
from reviews.models import Title, Category, Genre
from .permissions import IsAdminOrSafeMethod, IsAdmin
from .serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer,
    SignupSerializer,
    AdminSerializer,
    TokenSerializer,
    UserSerializer,
)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer    
    permission_classes = (IsAdminOrSafeMethod,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer    
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSafeMethod,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer   
    lookup_field = 'slug'
    permission_classes = (IsAdminOrSafeMethod,)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
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
              settings.DEFAULT_FROM_EMAIL,
              [email],
              )
    return Response({'email': email, 'username': username})


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(CustomUser, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token_user = AccessToken.for_user(user)
        return Response({'Ваш токен':
                        f'{token_user}'}, status=status.HTTP_200_OK)
    return Response('', status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdmin, )
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
