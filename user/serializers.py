from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with that email already exists.')
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('A user with that username already exists.')
        return value
    
    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['username'] = validated_data['username'].lower()
        
        password = validated_data.pop('password', None)
        user = super().create(validated_data)        
        if password:
            user.set_password(password)
            user.save()
        return user