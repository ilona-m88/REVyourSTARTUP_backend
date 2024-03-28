from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *


# Serializer for Django Built-in User class
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MainFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainForm
        fields = '__all__'


class RevFormSerializer(serializers.ModelSerializer):    
    class Meta:
        model = RevForm
        fields = '__all__'


class RevFormRowsIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevFormRowsIndex
        fields = '__all__'


class RevFormRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevFormRows
        fields = '__all__'


class ProFormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProForma
        fields = '__all__'


class ProFormaFoundersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProFormaFounders
        fields = '__all__'
        