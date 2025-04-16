# forms.py
from django import forms
import uuid
from .models import Laptop,  Product, User
from myapp.services.credentials_service import CredentialsService


class LaptopForm(forms.ModelForm):
    """
    Class that represents a form for Laptop in process of it's adding to db
    """
    class Meta:
        """
        Internal class for setting a form for Laptop
        """

        # get all fields from db's Laptops table
        model = Laptop

        # setting input boxes for all of them
        fields = '__all__'

        # setting input format for some fields
        widgets = {
            'screen_size': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '13.3',
                'max': '90'
            }),
            'scree_resolution': forms.TextInput(attrs={
                'placeholder': '1920x1080',
                'pattern': r'^\d{3,4}x\d{3,4}$'
            }),
            'screen_ref_rate': forms.NumberInput(attrs={
                'min': '60',
                'max': '240'
            }),
            'cpu_model': forms.TextInput(attrs={
                'placeholder': 'Ryzen 5 5600H'
            }),
            'cpu_cores_num': forms.NumberInput(attrs={
                'min': '2',
                'max': '20'
            }),
            'cpu_frequency': forms.NumberInput(attrs={
                'step': '0.1',
                'max': '40'
            }),
            'ram': forms.NumberInput(attrs={
                'min': '2',
                'step': '2',
                'max': '40'
            }),
            'ram_type': forms.TextInput(attrs={
                'placeholder': 'DDR4',
                'maxlength': '5'
            }),
            'storage': forms.NumberInput(attrs={
                'step': '10',
                'min': '120',
                'max': '2000'
            }),
            'storage_type': forms.TextInput(attrs={
                'placeholder': 'SSD',
                'maxlength': '5'
            }),
            'gpu_model': forms.TextInput(attrs={
                'placeholder': 'RTX 3060',
                'maxlength': '15'
            }),
        }


class ProductForm(forms.ModelForm):
    """
    Class that represents a form for Product in process of it's adding to db
    """
    class Meta:
        """
        Internal class for setting a form for Product
        """

        # get all fields from db's Product table
        model = Product

        # exclude 2 fields which are setting later
        exclude = ['category_prod_id', 'category']

        # setting input format for some fields
        widgets = {
            'model_name': forms.TextInput(attrs={
                'placeholder': 'Acer Nitro 5',
                'maxlength': '30'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Опис моделі...'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '5000',
                'max': '120000'
            }),
        }


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

        # hashing the password using a custom service
        user.password = CredentialsService.hash_password(
            self.cleaned_data['password1']
        )

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
