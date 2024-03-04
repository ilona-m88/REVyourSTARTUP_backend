from django.urls import path
from .views import *

urlpatterns = [
    # Health Check Endpoint
    path('home/', HealthCheckAPIView.as_view()),
    
    # Registration Endpoint
    path('register/', RegisterNewUserView.as_view()),

    # Login Endpoint
    path('login/', UserLoginView.as_view()),
    
    # List all Users in the Database Endpoint
    path('users/', ListAllUsersView.as_view()),

    # Get a User from the database by id
    path('users/<int:id>', GetUserByIDView.as_view()),
]