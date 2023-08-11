import uuid

from rest_framework import serializers
from .models import StockHistory
from profiles.serializers import ProfileSerializer, ProfileField
from profiles.models import Profile
from aircraft.serializers import AircraftSerializer, AircraftField
from aircraft.models import Aircraft
from ac_stock.models import StockRecord
from ac_stock.serializers import StockRecordSerializer, StockRecordField


class StockHistorySerializer(serializers.ModelSerializer):
    created_by = ProfileField(queryset=Profile.objects.all())
    stock_record = StockRecordField(queryset=StockRecord.objects.all())
    # created_by = ProfileSerializer(many=False, read_only=True)
    # aircraft = AircraftSerializer(many=False, read_only=True)

    class Meta:
        model = StockHistory
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(rep)
        rep['created_by'] = str(rep['created_by'])
        rep['stock_record'] = str(rep['stock_record'])
        # created_by_instance = rep.get('created_by')
        # stock_instance = rep.get('stock_record')
        # if isinstance(created_by_instance, uuid.UUID):
        #     profile = Profile.objects.get(id=created_by_instance)
        #     rep['created_by'] = ProfileSerializer(profile).data
        # if isinstance(stock_instance, uuid.UUID):
        #     stock = StockRecord.objects.get(id=stock_instance)
        #     rep['stock_record'] = StockRecordSerializer(stock).data
        #
        # rep['created_by'] = ProfileSerializer(created_by_instance).data
        # rep['aircraft'] = AircraftSerializer(aircraft_instance).data
        return rep

    def create(self, validated_data):
        created_by_data = validated_data.pop('created_by')
        stock_data = validated_data.pop('stock_record')
        if isinstance(created_by_data, uuid.UUID):
            created_by_instance = Profile.objects.get(id=created_by_data)
        else:
            created_by_instance = created_by_data

        if isinstance(stock_data, uuid.UUID):
            stock_instance = StockRecord.objects.get(id=stock_data)
        else:
            stock_instance = stock_data

        stock_history_instance = StockHistory.objects.create(created_by=created_by_instance, stock_record=stock_instance, **validated_data)
        return stock_history_instance