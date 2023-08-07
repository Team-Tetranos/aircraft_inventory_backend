import json

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Profile
from rest_framework import serializers
from utility.uuid_encoder import UUIDEncoder

from aircraft.serializers import AircraftNameSerializer, AircraftSerializer

from aircraft.models import Aircraft


class ProfileSerializer(ModelSerializer):
    permitted_aircrafts = AircraftSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))


