from django.db import models
from django.contrib.auth import get_user_model

# from accounts.models import User

# getting the User model from the settings.py file
# User = get_user_model()

# Create your models here.


class Post(models.Model):

    """
    this is a class to define posts for blog app
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/blog/posts/', null=True, blank=True)
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
