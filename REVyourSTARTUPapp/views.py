from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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


class UserLoginView(APIView):
    # Simple authentication view using Djangos built-in User class and authentication() function

    # TODO: Should include some kind of tokenization in order to keep track of users session
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Backend authenticated credentials
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                message = "User is inactive"
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Credentials were not authenticated
            message = "Unable to authenticate user"
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    # Simple Logout View
    # TODO: This should be finished once there is some functionality associated with cookies, session, etc..
    def post(self, request):
        username = request.data.get("username")


class ListAllUsersView(ListAPIView):
    # Generic View for listing all users in the database
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetUserByIDView(APIView):
    # View demonstrating how to use a serializer to get a user by their id
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
