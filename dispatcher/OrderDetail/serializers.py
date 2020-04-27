from rest_framework import serializers
from .models import *

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id','user', 'from_address', 'to_address', 'status', 'tracking', 'category', 'item_info', 'capacity', 'create_time',  'depart_time', 'pickup_time', 'complete_time', 'station', 'shipping_method', 'shipping_number', 'total_cost', 'feedback')
