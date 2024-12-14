import pytest
from django.urls import reverse

from ..models import User

from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestAccountUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

