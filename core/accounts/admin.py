from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Profile
from django.utils.translation import gettext_lazy as _


# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Groups', {'fields': ('groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)})
    ]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'bio')
    # list_filter = ('user',)
    # search_fields = ('user',)
    # ordering = ('user',)
    # fieldsets = [
    #     (None, {'fields': ('user', 'phone_number', 'address')}),
    # ]
    # add_fieldsets = (
    #     (None, {
    #         "classes": ("wide",),
    #         "fields": (
    #             "user", "phone_number", "address"
    #         )}
    #      ),
    # )
