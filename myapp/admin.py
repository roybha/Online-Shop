from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Configuring the display of the User model in the Django admin panel
    """

    # forms for creating and editing users

    # form used when creating a new user
    add_form = UserCreationForm

    # form used when editing a user
    form = UserChangeForm

    # the model represented by this admin class
    model = User

    # fields that will be displayed in the user list
    list_display = ('email', 'role', 'is_staff', 'is_active')

    # filters in the right panel in the admin
    list_filter = ('is_staff', 'is_active', 'role')

    # searchable fields
    search_fields = ('email',)

    # default user sorting (by email)
    ordering = ('email',)

    # grouping fields in a user edit form
    fieldsets = (

        # main information
        (None, {'fields': ('email', 'password')}),
        ('Персональна інформація', {'fields': ('role',)}),
        ('Права доступу', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Інше', {'fields': ('last_login',)}),
    )

    # fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'role',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )


# registering a custom User's model in the admin area
admin.site.register(User, UserAdmin)
