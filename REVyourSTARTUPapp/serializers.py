from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


# Serializer for Django Built-in User class
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'