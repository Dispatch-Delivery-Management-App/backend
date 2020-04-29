from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)
    firstname = models.CharField(max_length=30, null=True)
    lastname = models.CharField(max_length=30, null=True)
    token = models.CharField(max_length=255, null=True)
