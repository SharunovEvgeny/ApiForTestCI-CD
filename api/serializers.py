from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Chat


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )

class chatSerializer(serializers.ModelSerializer):
    #user =userSerializer(read_only=True, many=True)
    class Meta:
        model = Chat
        fields = (
            'numberOfPeople',
            'name',
            'id',
        )

class messageSerializer(serializers.ModelSerializer):
    user =userSerializer(read_only=True)
    class Meta:
        model = Message
        fields = (
            'user',
            'text',
            'data',
        )