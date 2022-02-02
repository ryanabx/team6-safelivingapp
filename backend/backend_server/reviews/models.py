from django.db import models


# Create your models here.
class Review (models.Model):
    city = models.CharField("city", max_length=256)
    state = models.CharField("state", max_length=256)
    rating = models.IntegerField()
    text = models.CharField("text", max_length=256)

