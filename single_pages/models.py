from django.db import models
import os


# 웹크롤링
class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)


# Create your models here.
