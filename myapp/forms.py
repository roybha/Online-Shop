# forms.py
from django import forms
from .models import Laptop,  Product


class LaptopForm(forms.ModelForm):
    """
    Class that represents a form for Laptop in process of it's adding to db
    """

    #special field for cpu brand input
    cpu_brand_name = forms.CharField(
        max_length=50,
        label='CPU бренд',
        widget=forms.TextInput(attrs={'placeholder': 'AMD'})
    )

    # special field for gpu brand input
    gpu_brand_name = forms.CharField(
        max_length=50,
        label='GPU бренд',
        widget=forms.TextInput(attrs={'placeholder': 'NVIDIA'})
    )

    class Meta:
        """
        Internal class for setting a form for Laptop
        """

        # get all fields from db's Laptops table
        model = Laptop

        # setting input boxes for all of them
        exclude = ['gpu_brand', 'cpu_brand']

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

    # special field for input brand name
    brand_name = forms.CharField(
        max_length=50,
        label='Бренд',
        widget=forms.TextInput(attrs={
            'placeholder': 'Acer',
            'maxlength': '50'
        })
    )
    class Meta:
        """
        Internal class for setting a form for Product
        """

        # get all fields from db's Product table
        model = Product

        # exclude 2 fields which are setting later
        exclude = ['category_prod_id', 'category', 'brand']

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
            'image_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/image.jpg'
            }),
        }
