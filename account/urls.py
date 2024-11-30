from django.urls import path
from account.views import UserLoginView,UserRegistrationView,UserListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),  # path for registration
    path('login/', UserLoginView.as_view(),name='Login'),
    path('userlist/',UserListView.as_view(),name="user list"),
]