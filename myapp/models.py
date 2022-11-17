from django.db import models

class movie(models.Model):
    title = models.CharField(max_length=100,unique=True)
    year = models.CharField(max_length=100,unique=False)
    userRating = models.FloatField()
    link = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200)
    popularity = models.FloatField()

class scoreboard(models.Model):
    pass



