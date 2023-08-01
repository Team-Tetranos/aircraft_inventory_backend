from rest_framework.serializers import ModelSerializer
from .models import Aircraft, AircraftItem


class AircraftSerializer(ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'


class AircraftItemSerializer(ModelSerializer):
    class Meta:
        model = AircraftItem
        fields = '__all__'
