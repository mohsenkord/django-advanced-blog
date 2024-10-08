from django.urls import path, include
from .views import PostListView, PostDetailView, ContactView, PostCreateView

app_name = 'blog'

urlpatterns = [
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('api/v1/', include('blog.api.v1.urls')),
]
