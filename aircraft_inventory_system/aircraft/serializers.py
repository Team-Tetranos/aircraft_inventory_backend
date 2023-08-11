import uuid

from rest_framework import serializers
from .models import Aircraft, AircraftItem



class AircraftField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            aircraft_id = uuid.UUID(data)
            aircraft_instance = Aircraft.objects.get(id=aircraft_id)
            return aircraft_instance
        except (ValueError, Aircraft.DoesNotExist):
            raise serializers.ValidationError("Invalid Aircraft ID")

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftItem
        fields = '__all__'


class AircraftNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['name']
