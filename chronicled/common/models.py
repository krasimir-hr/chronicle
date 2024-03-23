from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from chronicled.games.models import Game

UserModel = get_user_model()


class Review(models.Model):
    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    date_time_posted = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )


class Like(models.Model):
    to_review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

class Comment(models.Model):
    to_review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    text = models.TextField(
        max_length=300,
    )

    date_time_posted = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date_time_posted']


class Log(models.Model):
    PROGRESS_CHOICES = (
        (1, 'Completed'),
        (2, 'Playing'),
    )

    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    date_posted = models.DateField(
        auto_now_add=True
    )

    review_text = models.TextField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )
