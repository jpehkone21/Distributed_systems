# users/serializers.py
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()