from django.db import models
from django.contrib.auth import get_user_model
CustomUser = get_user_model()


class Review(models.Model):

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews'),
    text = models.TextField(max_length=3000)
    score = models.ForeignKey('Score', on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_title_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']


class Score(models.Model):
    SCORE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='scores')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_title_score'
            )
        ]
