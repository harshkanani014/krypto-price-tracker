from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
  
urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name="sign_up"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
]