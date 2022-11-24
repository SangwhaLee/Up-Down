from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# 유효성 검증 중, 최소/최댓값에 대한 검증을 하는 validator

class Movie(models.Model):
    title = models.CharField(max_length=100,unique=True)
    year = models.CharField(max_length=100,unique=False)
    userRating = models.FloatField()
    link = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200)
    popularity = models.FloatField()

class Scoreboard(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])



