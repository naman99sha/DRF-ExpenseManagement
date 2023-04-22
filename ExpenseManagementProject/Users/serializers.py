from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        pw = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if pw is not None:
            instance.set_password(pw)
        instance.save()
        return instance