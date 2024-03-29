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

    @property
    def average_rating(self):
        avg_r = self.logs.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0

        if int(avg_r) == avg_r:
            avg_r = int(avg_r)

        return avg_r

