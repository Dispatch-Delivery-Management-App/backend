from rest_framework import serializers
from .models import *

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id','user', 'from_address', 'to_address', 'status', 'tracking', 'category', 'itemInfo', 'capacity', 'createTime',  'departTime', 'pickupTime', 'completeTime', 'station', 'shipping_method', 'shipping_number', 'total_cost', 'feedback')
