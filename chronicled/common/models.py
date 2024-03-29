from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from chronicled.games.models import Game

UserModel = get_user_model()


class Log(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]

    PLATFORM_NAMES = {
        '1': 'Unknown',
        '6': 'PC',
        '14': 'Mac',
        '18': 'NES',
        '19': 'SNES',
        '4': 'NINTENDO 64',
        '21': 'NINTENDO GameCube',
        '5': 'NINTENDO Wii',
        '41': 'NINTENDO Wii U',
        '130': 'NINTENDO Switch',
        '7': 'PS1',
        '2': 'PS2',
        '3': 'PS3',
        '48': 'PS4',
        '167': 'PS5',
        '12': 'XBOX 360',
        '49': 'XBOX ONE',
        '169': 'XBOX SERIES X|S',
        '32': 'SEGA SATURN',
        '29': 'SEGA GENESIS',
    }

    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE,
        related_name='logs'
    )

    rating = models.IntegerField(
        default=1,
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    date_posted = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    review_text = models.TextField(
        null=True,
        blank=True,
    )

    completed = models.BooleanField(
        default=True,
    )

    first_time = models.BooleanField(
        default=True,
    )

    platform_id = models.CharField(
        max_length=20,
    )
    
    def __str__(self):
        return f'Log for {self.game.name} by {self.user}'

    @property
    def get_platform_name(self):
        return self.PLATFORM_NAMES[self.platform_id]
    


class Like(models.Model):
    to_log = models.ForeignKey(
        to=Log,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

class Comment(models.Model):
    to_log = models.ForeignKey(
        to=Log,
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