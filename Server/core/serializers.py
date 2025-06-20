from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField()
    def create(self, validated_data):
        from .models import User  
        return User(**validated_data).save()
