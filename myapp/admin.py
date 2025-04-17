import uuid
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User
from .services.credentials_service import CredentialsService


class UserCreationForm(forms.ModelForm):
    """
    Class for user creation form for the admin panel.
    Adds two password fields and checks if they match
    """

    # first password entry field
    password1 = forms.CharField(
        label='Пароль',

        # used for hidden input
        widget=forms.PasswordInput
    )

    # second field for verification of password
    password2 = forms.CharField(
        label='Підтвердження пароля',

        # also used for hidden input
        widget=forms.PasswordInput
    )

    class Meta:
        """
        Internal class for setting a form for User creation
        """

        # related user model
        model = User

        # fields that are displayed in the form
        fields = ('email', 'role')

    def clean_password2(self):
        """
        Method for check that both passwords match.
        If not, a validation error is thrown.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не збігаються")
        return password2

    def save(self, commit=True):
        """
        Method for saving a user with a hashed password
        and an automatically generated username.
        """

        # create the user object, but we don't save it to the database yet
        user = super().save(commit=False)

        # get role choice made by admin
        role = self.cleaned_data.get("role")

        # hashing the password using a custom service
        if role == 'admin':
            user.set_password(self.cleaned_data["password1"])
        else:
            user.password = CredentialsService.hash_password(self.cleaned_data["password1"])

        # generating username from email (before @) +
        # random six-character suffix
        user.username = f'{user.email.split("@")[0]}_{uuid.uuid4().hex[:6]}'
        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """
    Class for user edit form in the admin.
    Includes all important fields, including access statuses.
    """
    class Meta:
        """
        Internal class for setting a form for User change
        """

        # related model
        model = User

        # fields that will be represented fot changing
        fields = (
            'email',
            'password',
            'role',
            'is_active',
            'is_staff',
            'is_superuser'
        )


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
