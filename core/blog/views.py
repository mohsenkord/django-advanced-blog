from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post

# Create your views here.
class PostListView(LoginRequiredMixin, ListView):

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 5


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    template_name = 'blog/post_create.html'
    # fields = ['title', 'content', 'author', 'status']
    form_class = PostForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):

    model = Post
    template_name = 'blog/post_update.html'
    # fields = ['title', 'content', 'status']
    form_class = PostForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    template_name = 'blog/post_delete.html'
    success_url = '/blog/'