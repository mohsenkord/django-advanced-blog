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

    # send email urls
    path('send-email/', views.SendEmailView.as_view(), name='send_email'),

    # activation urls
    path('activation/confirm/<str:token>', views.ActivationAPIView.as_view(), name='activate'),

    # resend activation urls
    path('activation/resend-activation/', views.ResendActivationAPIView.as_view(), name='resend_activation'),

    # change password urls
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),

    # Send password recovery email urls
    path('password/recovery/', views.PasswordRecoveryAPIView.as_view(), name='password_recovery'),
    path('password/reset-confirm/<str:token>', views.PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),


    # jwt urls
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
