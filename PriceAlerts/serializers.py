from rest_framework import serializers
from .models import *


# Serializer to create, delete Current Alerts
class UserAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerts
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True},
        }

    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Serializer to create, delete Backup Alerts
class BackupAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllBackupAlerts
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True},
        }

    def create(self, validated_data): 
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Serializer to get all alerts
class GetAllAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllBackupAlerts
        fields = '__all__'
        extra_kwargs = {
            'id':{'read_only': True},
            'created_on':{'read_only': True},
        }