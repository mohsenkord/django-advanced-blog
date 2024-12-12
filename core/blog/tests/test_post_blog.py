import pytest
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from django.utils import timezone

from ..models import Post, Category
from ..api.v1.serializers import PostSerializer, CategorySerializer
from accounts.models import Profile, User
from accounts.api.v1.serializers import ProfileSerializer


@pytest.mark.django_db
class TestPostBlog:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(name='Test Category')
        self.client.force_authenticate(user=self.user)

    def test_get_posts(self):
        url = reverse("blog:api_v1:post-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_post(self):
        url = reverse("blog:api_v1:post-list")
        data = {
            "title": "Test post",
            "content": "Test content",
            "status": True,
            "published_date": timezone.now(),
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        post = Post.objects.get(title="Test post")
        assert post.title == "Test post"
        assert post.content == "Test content"
        assert post.status
        assert post.published_date

        wsgi_request = self.factory.get(reverse("blog:api_v1:post-detail", args=[post.pk]))
        wsgi_request.user = self.user
        request = Request(wsgi_request)
        request.parser_context = {
            'kwargs': {'pk': post.pk},
            'view': None,
        }

        serializer = PostSerializer(post, context={"request": request})
        assert serializer.data["title"] == "Test post"
        assert serializer.data["content"] == "Test content"
        assert serializer.data["status"]
        assert serializer.data["published_date"]

        profile = Profile.objects.get(user=self.user)
        assert profile.user.email == "testuser@gmail.com"

        profile_serializer = ProfileSerializer(profile)
        assert profile_serializer.data["email"] == "testuser@gmail.com"

        category = Category.objects.get(name="Test Category")
        assert category.name == "Test Category"

        category_serializer = CategorySerializer(category)
        assert category_serializer.data["name"] == "Test Category"

    def test_update_post(self):
        post = Post.objects.create(
            title="Test post",
            content="Test content",
            status=True,
            published_date=timezone.now(),
            author=Profile.objects.get(user=self.user),
        )
        url = reverse("blog:api_v1:post-detail", args=[post.pk])
        data = {
            "title": "Updated post",
            "content": "Updated content",
            "status": False,
            "published_date": timezone.now(),
        }
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

        post.refresh_from_db()
        assert post.title == "Updated post"
        assert post.content == "Updated content"
        assert not post.status
        assert post.published_date

    def test_delete_post(self):
        post = Post.objects.create(
            title="Test post",
            content="Test content",
            status=True,
            published_date=timezone.now(),
            author=Profile.objects.get(user=self.user),
        )
        url = reverse("blog:api_v1:post-detail", args=[post.pk])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
