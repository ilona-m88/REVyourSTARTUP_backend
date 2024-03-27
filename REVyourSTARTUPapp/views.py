from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .dataparse import *


class HealthCheckAPIView(APIView):
    def get(self, request):
        response = {'Message': "Hello, Yibran"}
        return Response(response, status=status.HTTP_200_OK)
    

class MakeSuperUserView(APIView):
    # This should only be used to make yourself a superuser in order to access the /admin functionality
    def put(self, request):
        username = request.data.get("username")
        user = User.objects.get(username=username)

        if user:
            user.is_superuser = 1
            user.is_staff = 1
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)

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

        user = authenticate(request, username=username, password=password)
        
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
        logout(request)
        return Response(status=status.HTTP_200_OK)


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


class CreateMainFormView(APIView):
    # View which allows the main form to be created and linked to a user's id
    # JSON
    # {
    #   'user_id': 1,
    #   'form_name': 'Sample Form Name'
    # }

    def post(self, request):
        user_id = request.data.get('user_id')
        form_name = request.data.get("form_name")
        user = get_object_or_404(User, id=user_id)
        if form_name:
            serializer = MainFormSerializer(data={'user': user.id, 'form_name': form_name})
        else:
            serializer = MainFormSerializer(data={'user': user.id})

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetMainFormByUserView(APIView):
    # View should be passed the User's id in the endpoint link, it will search for all the 
    # MainForm's associated with that id, and return a list of all the MainForm objects corresponding
    # to that specific User

    def get(self, request, id):
        try:
            queryset = MainForm.objects.get(user_id=id)
            serializer = MainFormSerializer(queryset)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except MainForm.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)
        
    # The post request should contain the User's id in the enpoint link, and also have the "form_name"
    # sent as a JSON, otherwise the response will be an error
    def post(self, request, id):
        form_name = request.data.get("form_name")
        user = get_object_or_404(User, id=id)
        if form_name:
            serializer = MainFormSerializer(data={'user': user.id, 'form_name': form_name})
        else:
            error = "Error: field 'form_name' missing from request"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RevFormView(APIView):
    # This view should handle the rev form in terms of GET, POST, PUT, and adhere to the JSON format
    # given in dataStructure_RevForm.json

    def post(self, request, mainform_id):
        # Parse the JSON starting with the outer-most tags
        valuation_data = request.data.get('valuationParameters')
        reality_check = request.data.get('realityCheck1')
        customer_segments_year3 = request.data.get('customerSegmentsYear3')
        customer_segments_year2 = request.data.get('customerSegmentsYear2')
        customer_segments_year1 = request.data.get('customerSegmentsYear1')

        if valuation_data is None or reality_check is None or customer_segments_year3 is None or customer_segments_year2 is None or customer_segments_year1 is None:
            # If either of these tags are missing, create an error and return a BAD_REQUEST Response
            error = 'Invalid request: Data is either mislabeled or missing entirely'
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Otherwise parse through the nested tags and create a serializer object for database 
            # storage. Also, should check for the validation of the data being stored

            # This is for testing pusposes only!
            #data_dict = {'valuationParameters': valuation_data, 'realityCheck1': reality_check}

            # This line is for parsing the json data in terms of the outer-most tags
            rev_form_data_dict = flatten_revform_json(valuation_data, reality_check)

            try:
                # Use flattened data_dict to serialize and, if valid, save in the database
                revform_serializer = RevFormSerializer(data=rev_form_data_dict)
                if revform_serializer.is_valid():
                    revform_serializer.save()

                    # Parse through all 3 of the customer_segments, create the appropriate 
                    # rev_form_row_index table, and all the corresponding revform_row tables

                    # YEAR 1
                    data_dict_year1 = flatten_revform_rows_json(customer_segments_year1, 'customerSegmentsYear1')
                    rev_form_rows_index_year1_serializer = RevFormRowsIndexSerializer(data=data_dict_year1['RevFormRowsIndex'])
                    if rev_form_rows_index_year1_serializer.is_valid():                      
                        rev_form_rows_index_year1_serializer.save()
                        rev_form_rows_index_year1_pk = rev_form_rows_index_year1_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year1_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year1_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year1['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year1_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

                    # YEAR 2
                    data_dict_year2 = flatten_revform_rows_json(customer_segments_year2, 'customerSegmentsYear2')
                    rev_form_rows_index_year2_serializer = RevFormRowsIndexSerializer(data=data_dict_year2['RevFormRowsIndex'])
                    if rev_form_rows_index_year2_serializer.is_valid():                      
                        rev_form_rows_index_year2_serializer.save()
                        rev_form_rows_index_year2_pk = rev_form_rows_index_year2_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year2_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year2_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year2['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year2_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
                    
                     # YEAR 3
                    data_dict_year3 = flatten_revform_rows_json(customer_segments_year3, 'customerSegmentsYear3')
                    rev_form_rows_index_year3_serializer = RevFormRowsIndexSerializer(data=data_dict_year3['RevFormRowsIndex'])
                    if rev_form_rows_index_year3_serializer.is_valid():                      
                        rev_form_rows_index_year3_serializer.save()
                        rev_form_rows_index_year3_pk = rev_form_rows_index_year3_serializer.data['revform_rows_index_id']
                        RevFormRowsIndex.objects.filter(revform_rows_index_id=rev_form_rows_index_year3_pk).update(rev_form=revform_serializer.data['rev_form_id'])
                    else:
                        return Response(rev_form_rows_index_year3_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    row_data_dict = data_dict_year3['RevFormRows']
                    for key in row_data_dict.keys():
                        rev_form_row_serializer = RevFormRowsSerializer(data=row_data_dict[key])
                        if rev_form_row_serializer.is_valid():
                            rev_form_row_serializer.save()
                            rev_form_row_pk = rev_form_row_serializer.data['revform_rows_id']
                            RevFormRows.objects.filter(revform_rows_id=rev_form_row_pk).update(revform_rows_index=rev_form_rows_index_year3_serializer.data['revform_rows_index_id'])
                        else:
                            error = "Row {} serializer failed to validate".format(key)
                            error_response = {"Message": error, "Serializer": rev_form_row_serializer.errors}
                            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


                    # Update the appropriate MainForm with the newly created RevForm as a foreign key
                    MainForm.objects.filter(main_form_id=mainform_id).update(rev_form=revform_serializer.data['rev_form_id'])
                    return Response(revform_serializer.data, status=status.HTTP_201_CREATED)     
                else:
                    return Response(revform_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except MainForm.DoesNotExist as exception:
                return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
            

    def get(self, request, mainform_id):
        # Get the Main Form and the associated RevForm and RevFormIndex by the given mainform_id
        try:
            mainform = MainForm.objects.get(main_form_id=mainform_id)
            revform = RevForm.objects.get(rev_form_id=mainform.rev_form.rev_form_id)
            revform_index = RevFormRowsIndex.objects.filter(rev_form=revform.rev_form_id)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the multiple RevFormIndex objects for parsing
        revform_index_serializer = RevFormRowsIndexSerializer(revform_index, many=True)

        # Parse the individual RevFormIndex Objects by their revform_rows_name and populate 
        # new variables with the appropriate data
        for i in range(len(revform_index_serializer.data)):
            if revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear1":
                customer_segments_year1 = revform_index_serializer.data[i]
            elif revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear2":
                customer_segments_year2 = revform_index_serializer.data[i]
            elif revform_index_serializer.data[i]["revform_rows_name"] == "customerSegmentsYear3":
                customer_segments_year3 = revform_index_serializer.data[i]

        # Given each RevFormIndex, get all the related RevFormRow objects associated with it,
        # serialize all of them, and then build the segment's "customerSegmentsYearx" json
        try:
            year1_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year1["revform_rows_index_id"])
            year1_rows_serializer = RevFormRowsSerializer(year1_rows, many=True)
            year1_customer_segment_json = build_customer_segments_json(customer_segments_year1, year1_rows_serializer.data)

            year2_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year2["revform_rows_index_id"])
            year2_rows_serializer = RevFormRowsSerializer(year2_rows, many=True)
            year2_customer_segment_json = build_customer_segments_json(customer_segments_year2, year2_rows_serializer.data)
            
            year3_rows = RevFormRows.objects.filter(revform_rows_index=customer_segments_year3["revform_rows_index_id"])        
            year3_rows_serializer = RevFormRowsSerializer(year3_rows, many=True)
            year3_customer_segment_json = build_customer_segments_json(customer_segments_year3, year3_rows_serializer.data)
        except Exception as exception:
            return Response(str(exception), status=status.HTTP_404_NOT_FOUND)

        # Pass the RevForm, and all the customerSegmentsYearx json's to be built into the correct
        # response format
        built_revform = build_revform_json(revform, year1_customer_segment_json, year2_customer_segment_json, year3_customer_segment_json)
        return Response(built_revform, status=status.HTTP_200_OK)
    


class TestRowFlattenEndpoint(APIView):
    # THIS ENDPOINT IS FOR TEST PURPOSES ONLY!!

    def post(self, request):
        customer_segments_year3 = request.data.get('customerSegmentsYear3')
        customer_segments_year2 = request.data.get('customerSegmentsYear2')
        customer_segments_year1 = request.data.get('customerSegmentsYear1')

        data_dict_year1 = flatten_revform_rows_json(customer_segments_year3, 'customerSegmentsYear3')

        return Response(data_dict_year1, status=status.HTTP_202_ACCEPTED)
    
