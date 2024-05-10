from django.contrib import admin
from .models import Post,Category


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ['title', 'author', 'updated_date', 'status']
    list_filter = ['status', 'created_date', 'updated_date']
    search_fields = ['title','content','author']
    raw_id_fields = ['author']
    date_hierarchy = 'updated_date'
    ordering = ['-updated_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name']