from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register your models here.


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('email', 'is_staff', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_verified')}),
        ('Important dates', {'fields': ('last_login','created_at', 'updated_at',)}),
        ('Groups Permissions', {'fields': ('groups', 'user_permissions',)}),
    )
    readonly_fields = ('last_login','created_at', 'updated_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'description', 'image')
    list_filter = ('user', 'first_name', 'last_name', 'description', 'image')
    search_fields = ('user', 'first_name', 'last_name', 'description', 'image')
    ordering = ('user', 'first_name', 'last_name', 'description', 'image')