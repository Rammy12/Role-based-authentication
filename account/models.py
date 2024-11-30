from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom manager for User model with methods to create regular and superusers.
    """
    def create_user(self, email, password=None, **extra_fields):
        # Ensure an email address is provided
        if not email:
            raise ValueError("Users must have an email address")
        
        # Normalize the email address (lowercase the domain part)
        email = self.normalize_email(email)
        
        # Create a user instance
        user = self.model(email=email, **extra_fields)
        
        # Set the password (hashed internally)
        user.set_password(password)
        
        # Save the user instance to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Method to create a superuser with default admin privileges and role 1.
        """
        # Ensure the superuser is staff and superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('role', 1)  # Set default role to Admin (1)
        
        # Validate that the role is set to Admin
        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        
        # Use the create_user method to create the superuser
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that supports roles and flexible authentication.
    """
    # Role definitions
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3

    # Role choices for the dropdown
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee')
    )

    # User attributes
    email = models.EmailField(unique=True)  # Email field must be unique
    first_name = models.CharField(max_length=255, blank=True)  
    last_name = models.CharField(max_length=255, blank=True) 
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)  # Default role is Employee
    is_active = models.BooleanField(default=True)  # Whether the user account is active
    is_staff = models.BooleanField(default=False)  # Whether the user has staff access
    is_superuser = models.BooleanField(default=False)  # Whether the user has superuser privileges
    date_joined = models.DateTimeField(auto_now_add=True)  # Auto-set the join date on creation

    # Link the custom manager
    objects = UserManager()

    # Define the unique identifier for authentication
    USERNAME_FIELD = 'email'  # Use email instead of username

    def __str__(self) -> str:
        # String representation of the user
        return self.email
