from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class CustomUser(AbstractUser):
    username = models.CharField(verbose_name='Имя пользователя',
                                unique=True,
                                max_length=150)
    email = models.EmailField(verbose_name='Почтовый ящик',
                              unique=True,
                              max_length=254)
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(verbose_name='Статус',
                            choices=UserRoles.choices,
                            max_length=30,
                            default=UserRoles.USER)
    confirmation_code = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = ''

