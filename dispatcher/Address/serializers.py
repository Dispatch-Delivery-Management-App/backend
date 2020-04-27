from rest_framework import serializers
from .models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','firstname', 'lastname', 'street', 'city', 'state', 'zipcode', 'phone')

class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressList
        fields = ('id','user','address')
