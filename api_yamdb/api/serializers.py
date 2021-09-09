from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import CustomUser


class SingupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(
                                       queryset=CustomUser.objects.all())])
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(
                                         queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
#
#
# class AdminSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True,
#                                      validators=[UniqueValidator(
#                                          queryset=CustomUser.objects.all())])
#
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'last_name', 'first_name', 'email',
#                     'role', 'bio')
#
#
# class UserSerializer(AdminSerializer):
#     role = serializers.CharField(readonly=True)
