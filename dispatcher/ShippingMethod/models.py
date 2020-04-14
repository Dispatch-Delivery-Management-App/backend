from django.db import models

class Drone(models.Model):
    name = models.CharField(max_length=30, null=True)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    capacity = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)

class Robot(models.Model):
    name = models.CharField(max_length=30, null=True)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    capacity = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
