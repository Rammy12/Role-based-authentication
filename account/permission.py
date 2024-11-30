from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    """
    Custom permission to allow only users with role 3 (Employee) to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        # Allow access if the user's role is Employee (3)
        return request.user.role == 3

class IsManager(BasePermission):
    """
    Custom permission to allow only users with role 2 (Manager) to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        # Allow access if the user's role is Manager (2)
        return request.user.role == 2

class IsAdmin(BasePermission):
    """
    Custom permission to allow only users with role 1 (Admin) to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        # Allow access if the user's role is Admin (1) 
        return request.user.role == 1

class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow only users with role 1 (Admin) or role 2 (Manager) to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        # Allow access if the user's role is Admin (1) or Manager (2)
        return request.user.role in [1,2]