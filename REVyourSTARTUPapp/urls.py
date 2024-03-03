from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HealthCheckAPIView.as_view()),
]