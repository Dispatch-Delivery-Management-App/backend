from rest_framework import serializers
from .models import *

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('id','name', 'street', 'city', 'state', 'zipcode', 'total_rating', 'rating_count', 'rating')

class StationDroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationDrone
        fields = ('id','station', 'drone', 'status')

class StationRobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationRobot
        fields = ('id','station', 'robot', 'status')
