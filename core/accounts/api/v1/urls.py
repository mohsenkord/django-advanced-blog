from django.urls import path, include
from . import views
# from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'api_v1'

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('token/login/', views.CustomAuthToken.as_view(), name='login'),
    path('token/logout/', views.CustomDestroyAuthToken.as_view(), name='logout'),
]