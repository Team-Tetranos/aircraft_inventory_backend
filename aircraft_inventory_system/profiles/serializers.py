import json

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Profile
from utility.uuid_encoder import UUIDEncoder


class ProfileSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))

