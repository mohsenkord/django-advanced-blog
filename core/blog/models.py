from django.db import models
# from django.contrib.auth import get_user_model
from django.urls import reverse
# from ..accounts.models import Profile
# Create your models here.

# getting user model
# User = get_user_model()


class Post(models.Model):
    """
    this a class to define posts for blog application
    """
    title = models.CharField(max_length=250)
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to="blog", null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[:5]

    def get_absolute_api_url(self):
        return reverse("blog:api_v1:post-detail", kwargs={"pk": self.pk})

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
