from rest_framework import serializers
from .models import Aircraft, AircraftItem


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftItem
        fields = '__all__'


