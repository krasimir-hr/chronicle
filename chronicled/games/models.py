from django.db import models


class Game(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )

    release_date = models.DateField()

    genres = models.JSONField()
    
    platforms = models.JSONField()

    cover = models.CharField(max_length=15)

    def average_rating(self):
        average_rating = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return average_rating if average_rating is not None else 0.0
    
    
