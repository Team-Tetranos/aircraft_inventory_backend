import uuid

from rest_framework import serializers
from rest_framework.utils import json

from .models import StockRecord
from profiles.serializers import ProfileSerializer, ProfileField
from profiles.models import Profile
from aircraft.serializers import AircraftSerializer, AircraftField
from aircraft.models import Aircraft

from stock_history.models import StockHistory

from utility.uuid_encoder import UUIDEncoder


class StockRecordField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            stock_id = uuid.UUID(data)
            stock_instance = StockRecord.objects.get(id=stock_id)
            return stock_instance
        except (ValueError, StockRecord.DoesNotExist):
            raise serializers.ValidationError("Invalid stock ID")


class StockRecordSerializer(serializers.ModelSerializer):
    created_by = ProfileField(queryset=Profile.objects.all())
    aircraft = AircraftField(queryset=Aircraft.objects.all())

    # created_by = ProfileSerializer(many=False, read_only=True)
    # aircraft = AircraftSerializer(many=False, read_only=True)

    class Meta:
        model = StockRecord
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(rep)
        created_by_instance = rep.get('created_by')
        aircraft_instance = rep.get('aircraft')
        if isinstance(created_by_instance, uuid.UUID):
            profile = Profile.objects.get(id=created_by_instance)
            rep['created_by'] = ProfileSerializer(profile).data
        if isinstance(aircraft_instance, uuid.UUID):
            aircraft = Aircraft.objects.get(id=aircraft_instance)
            rep['aircraft'] = AircraftSerializer(aircraft).data
        #
        # rep['created_by'] = ProfileSerializer(created_by_instance).data
        # rep['aircraft'] = AircraftSerializer(aircraft_instance).data
        return rep

    def create(self, validated_data):
        created_by_data = validated_data.pop('created_by')
        aircraft_data = validated_data.pop('aircraft')
        if isinstance(created_by_data, uuid.UUID):
            created_by_instance = Profile.objects.get(id=created_by_data)
        else:
            created_by_instance = created_by_data

        if isinstance(aircraft_data, uuid.UUID):
            aircraft_instance = Aircraft.objects.get(id=aircraft_data)
        else:
            aircraft_instance = aircraft_data

        stock_instance = StockRecord.objects.create(created_by=created_by_instance, aircraft=aircraft_instance,
                                                    **validated_data)
        return stock_instance


class StockHistorySerializerForReport(serializers.ModelSerializer):
    class Meta:
        model = StockHistory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))


class StockRecordSerializerForReport(serializers.ModelSerializer):
    stock_histories = StockHistorySerializerForReport(source='stockhistory_set', many=True, read_only=True)

    class Meta:
        model = StockRecord
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return json.loads(json.dumps(data, cls=UUIDEncoder))
