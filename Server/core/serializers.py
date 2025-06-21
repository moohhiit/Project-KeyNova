from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone = serializers.RegexField(regex=r'^\+?\d{10,15}$', required=True)
    password = serializers.CharField()
    secret_key = serializers.CharField(read_only = True)


    def create(self, validated_data):
        from .models import User    
        user  = User(**validated_data)
        user.save()
        return user
    

