from django.db import models


class Game(models.Model):
    slug = models.CharField(
        null=False,
        blank=False,
    )

    name = models.CharField(
        null=False,
        blank=False,
    )

    cover_id = models.CharField(
        null=False,
        blank=False
    )

def __str__(self):
    return self.name

