from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for the User model.

    Features:
    - Displays key user fields in the admin list view.
    - Allows searching and ordering by user ID, email, and name.
    - Organizes form fields into logical sections for viewing and editing.
    - Supports custom user creation form via add_fieldsets.

    Attributes:
        model: Specifies the custom User model.
        list_display: Fields displayed in the user list view in admin.
        search_fields: Fields that can be searched using the admin search bar.
        ordering: Default ordering of the user list.
        fieldsets: Field layout for viewing/editing a user.
        add_fieldsets: Field layout when adding a new user from the admin.
    """
    model = User
    list_display = ('user_id', 'email', 'name', 'role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('user_id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'profile_info', 'role', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(User, CustomUserAdmin)