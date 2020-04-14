from django.db import models

class Tracking(models.Model):
    street = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    zipcode = models.IntegerField(default=0, null=True)
