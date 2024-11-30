from account.serializers import UserSerializer,UserLoginSerializer,UserListSerializer
from account.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.permission import IsAdmin,IsEmployee,IsManager,IsAdminOrManager
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class UserRegistrationView(APIView):
    """
    View to Register users.
    """
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user to the database if the data is valid
            serializer.save()
            return Response({
                'message': 'User successfully registered!',
                'user': serializer.data
            },status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    """
    View to login users.
    """
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {
                    'message': 'User logged in successfully',
                    'access': serializer.validated_data['access'],
                    'refresh': serializer.validated_data['refresh'],
                    'user': {
                        'email': serializer.validated_data['email'],
                        'role': serializer.validated_data['role']
                    }
                },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class UserListView(APIView):
    """
    View to list all users.
    Only accessible to authenticated , admin and manager.
    """
    permission_classes=[IsAuthenticated,IsAdminOrManager]
    def get(self,request):
        # Query all user objects
        print(request.user.role)
        users=User.objects.all()
        serializer=UserListSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

