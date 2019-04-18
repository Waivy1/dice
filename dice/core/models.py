from django.db import models

class Dice(models.Model):
    name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255, null=True, default=None)

class Result1(models.Model):
    sum = models.CharField(max_length=10)
    user = models.CharField(max_length=10)

class User(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=20)