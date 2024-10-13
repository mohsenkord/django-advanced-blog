
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from ...models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'author']

class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
