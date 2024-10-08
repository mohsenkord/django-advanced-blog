from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, FormView, CreateView
)

from .models import Post
from .forms import ContactForm
# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'blog/contact.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'status', 'published_date']
    template_name = 'blog/post_create.html'
    success_url = '/blog/post/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

