from django.urls import path
from .views import *

urlpatterns = [
    # Health Check Endpoint
    path('home/', HealthCheckAPIView.as_view()),

    # Make superuser for existing account
    path('superuser/', MakeSuperUserView.as_view()),
    
    # Registration Endpoint
    path('register/', RegisterNewUserView.as_view()),

    # Login Endpoint
    path('login/', UserLoginView.as_view()),

    # Logout
    path('logout/', UserLogoutView.as_view()),
    
    # List all Users in the Database Endpoint
    path('users/', ListAllUsersView.as_view()),

    # Get a User from the database by id
    path('users/<int:id>', GetUserByIDView.as_view()),

    # Initial Creation of a Main Form
    path('form/', CreateMainFormView.as_view()),

    # POST: Create a new Main Form for user with id=id, GET: All Main Form's by a Users Id
    path('form/<int:id>', GetMainFormByUserView.as_view()),

    # RevForm endpoint
    path('form/rev_form/<int:mainform_id>', RevFormView.as_view()),

    # ProForma endpoint
    path('form/pro_forma/<int:mainform_id>', ProFormaView.as_view()),

    # TEST ENDPOINT
    path('test/', TestRowFlattenEndpoint.as_view()),
]