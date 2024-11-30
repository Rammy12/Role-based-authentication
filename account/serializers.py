from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles user creation and data validation.
    """
    password=serializers.CharField(write_only=True)
    def create(self,validated_data):
        """
        Custom method to create a user instance.
        """
        user=get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name',""), ## Optional first name, default to empty string
            last_name=validated_data.get('last_name',""), # Optional last name, default to empty string
            role=validated_data.get('role',3)  # Default role is 3 
        )
        return user
    class Meta:
        model=get_user_model()
        fields=['email','password','first_name','last_name','role']
        extra_kwargs={
            'password':{'write_only':True}   # password is write-only for API operations
            }


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Handles authentication and token generation.
    """
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self,data):
        """
        Custom validation for user login.
        Authenticates the user and generates tokens if credentials are valid.
        """
        email=data.get('email')
        password=data.get('password')

        if email is None:
            raise serializers.ValidationError("Email Address is required")
        
        if password is None:
            raise serializers.ValidationError("Password is required")
        
        user=authenticate(email=email,password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
        

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for user list.
    """
    class Meta:
        model=get_user_model()
        fields=['id','email','first_name','last_name','role']
    
