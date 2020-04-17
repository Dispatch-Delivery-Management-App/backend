from django.db import models
from ShippingMethod.models import Drone, Robot

class Station(models.Model):
    name = models.CharField(max_length=30, null=True)
    street = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    zipcode = models.IntegerField(default=0, null=True)
    total_rating = models.IntegerField(default=0, null=True)
    rating_count = models.IntegerField(default=0, null=True)
    rating = models.DecimalField(default=1.0, decimal_places=1, max_digits=2)


class StationDrone(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

class StationRobot(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
