import json

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Profile
from rest_framework import serializers
from utility.uuid_encoder import UUIDEncoder

from aircraft.serializers import AircraftNameSerializer, AircraftSerializer


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))
