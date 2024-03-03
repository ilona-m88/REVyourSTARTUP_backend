from django.shortcuts import render
from django.http import HttpRequest

from rest_framework.generics import get_object_or_404, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

# Create your views here.

class HealthCheckAPIView(APIView):
    def get(self, request):
        response = {'Message': "Hello, World!"}
        return Response(response, status=status.HTTP_200_OK)


