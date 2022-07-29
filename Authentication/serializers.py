from rest_framework import serializers
from django.contrib.auth.models import User
from hashlib import pbkdf2_hmac
from base64 import b64encode
import os


# User serializer for saving user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'id':{'read_only': True},
            'password':{'write_only': True}
        }

    def update(self, instance, validated_data):
        if(instance.password):
            for attr, value in validated_data.items():
                if attr == 'password' and value!=None:
                    instance.set_password(value)
                elif attr == 'password' and value==None:
                    pass
                else:
                    setattr(instance, attr, value)
            instance.save()
            return instance
        else:
            instance.save()
            return instance


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


