from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('', include('accounts.api.v1.urls.accounts')),
    path('profile/', include('accounts.api.v1.urls.profiles')),
]