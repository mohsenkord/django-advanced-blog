from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('token/login/', views.CustomAuthToken.as_view(), name='login'),
    path('token/logout/', views.CustomDestroyAuthToken.as_view(), name='logout'),

    # change password urls
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),

    # jwt urls
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
