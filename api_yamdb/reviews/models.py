from django.core.validators import ValidationError
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError('Год не может быть больше текущего')


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    year = models.IntegerField(
        verbose_name='Год публикации',
        validators=[
            year_validator
        ]
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        blank=True, null=True
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name="unique_genre_title")
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'
