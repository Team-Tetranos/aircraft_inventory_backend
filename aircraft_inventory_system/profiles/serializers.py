import json
import uuid

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Profile
from rest_framework import serializers
from utility.uuid_encoder import UUIDEncoder

from aircraft.serializers import AircraftNameSerializer, AircraftSerializer

from aircraft.models import Aircraft


class ProfileField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            profile_id = uuid.UUID(data)
            profile_instance = Profile.objects.get(id=profile_id)
            return profile_instance
        except (ValueError, Profile.DoesNotExist):
            raise serializers.ValidationError("Invalid profile ID")


class ProfileSerializer(ModelSerializer):
    permitted_aircrafts = AircraftSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))

    # def get_permitted_aircrafts(self, instance):
    #     permitted_aircrafts = instance.permitted_aircrafts.all()
    #     return AircraftSerializer(permitted_aircrafts, many=True).data
