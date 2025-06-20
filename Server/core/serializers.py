from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = serializers.CharField()
    password = serializers.CharField()
