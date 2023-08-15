from rest_framework import serializers
from .models import HelpDesk


class HelpDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpDesk
        fields = '__all__'
