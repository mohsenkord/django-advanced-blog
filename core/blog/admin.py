from django.contrib import admin
from .models import Post, Category
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ('title', 'author', 'created_date', 'updated_date', 'published_date')
    search_fields = ('title', 'author', 'created_date', 'updated_date', 'published_date')
    ordering = ('title', 'author', 'created_date', 'updated_date', 'published_date')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

