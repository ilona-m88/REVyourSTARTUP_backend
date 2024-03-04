from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import *

# Create your views here.

class HealthCheckAPIView(APIView):
    def get(self, request):
        response = {'Message': "Hello, World!"}
        return Response(response, status=status.HTTP_200_OK)


class RegisterNewUserView(APIView):
    # Simple registration view using Djangos built-in User class
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")


        user = User.objects.create_user(username, email, password)

        response = {'User_ID': user.id, 'Username': user.username, 'Email': user.email}
        return Response(response, status=status.HTTP_201_CREATED)


class ListAllUsersView(ListAPIView):
    # Generic View for listing all users in the database
    queryset = User.objects.all()
    serializer_class = UserSerializer
