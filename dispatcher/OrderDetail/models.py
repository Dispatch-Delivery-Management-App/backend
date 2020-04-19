from django.db import models
from User.models import User
from Address.models import Address
from Tracking.models import Tracking
from django.db.models import DateTimeField
from Station.models import Station

class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='fromaddress')
    to_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='toaddress')
    status = models.IntegerField(default=0)
    tracking = models.ForeignKey(Tracking, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, null=True)
    item_info = models.CharField(max_length=30, null=True)
    capacity = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    create_time = DateTimeField(auto_now=False, null=True)
    depart_time = DateTimeField(auto_now=False, null=True)
    pickup_time = DateTimeField(auto_now=False, null=True)
    complete_time = DateTimeField(auto_now=False, null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    shipping_method = models.CharField(max_length=30, null=True)
    shipping_number = models.IntegerField(default=1)
    total_cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    feedback = models.IntegerField(null=True)
