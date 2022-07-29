from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
  
urlpatterns = [
    path('create/', CreateAlert.as_view(), name="create_alert"),
    path('delete/<int:id>', DeleteAlert.as_view(), name="delete_alert"),
    path('get-alerts/', GetAllAlerts.as_view(), name="get_all_alerts") # Filters and pagination available
]