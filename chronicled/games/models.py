from django.db import models


class Game(models.Model):
    slug = models.CharField(
        null=False,
        blank=False,
    )

