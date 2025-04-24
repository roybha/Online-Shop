# forms.py
from cProfile import label

from django import forms
from .models import Laptop, Product, Smartphone


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
                'placeholder': '5600H'
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


class SmartphoneForm(forms.ModelForm):
    """
    Class that represents a form for Smartphone in process of it's adding to db
    """

    # possible list of values
    # for network generations
    NETWORK_GENERATION_CHOICES = [
        ('2G', '2G'),
        ('3G', '3G'),
        ('4G', '4G'),
        ('5G', '5G'),
    ]

    # make specified input field
    # for possible network generations
    network_generations = forms.MultipleChoiceField(
        choices=NETWORK_GENERATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Типи зв’язку"
    )
    class Meta:
        """
        Internal class for setting a form for Smartphone
        """

        # get fields from db's Smartphone table
        model = Smartphone

        # get all fields from Smartphone model
        fields = '__all__'

        widgets = {
            'screen_size': forms.NumberInput(attrs={
                'step': '0.1',
                'placeholder': '4.3',
                'max': '10'
            }),
            'scree_resolution': forms.TextInput(attrs={
                'placeholder': '1920x1080',
                'pattern': r'^\d{3,4}x\d{3,4}$'
            }),
            'screen_ref_rate': forms.NumberInput(attrs={
                'min': '60',
                'max': '240'
            }),
            'sim_quantity': forms.NumberInput(attrs={
                'min': '1',
                'step': '1',
                'max': '3'
            }),
            'cpu_model': forms.TextInput(attrs={
                'placeholder': '2400e',
            }),
            'cpu_cores_num': forms.NumberInput(attrs={
                'min': '4',
                'step': '1',
                'max': '12'
            }),
            'ram': forms.NumberInput(attrs={
                'min': '2',
                'step': '1',
                'max': '12'
            }),
            'storage': forms.NumberInput(attrs={
                'min': '64',
                'step': '1',
                'max': '256'
            }),
            'main_camera': forms.TextInput(attrs={
                'pattern': r'^(\d+\+)*\d+$',
            }),
            'max_video_resolution': forms.TextInput(attrs={
                'placeholder': 'Напр. 7680 x 4320 або 7680 x 4320 8K UHD',
                'pattern': r'^\d{3,5}\sx\s\d{3,5}(?:\s[\w\s]{2,15})?$'
            }),
            'frontal_camera': forms.TextInput(attrs={
                'placeholder': 'Наприклад, 8',
                'pattern': r'^\d+$',
                'title': 'Введіть фронтальну камеру як ціле число',
            }),
            'nfc': forms.CheckboxInput(),
            'connector_type': forms.TextInput(attrs={
                'placeholder':'Type-C'
            }),
            'battery': forms.NumberInput(attrs={
                'min': '500',
                'step': '100',
                'max': '6500'
            }),
            'weight': forms.NumberInput(attrs={
                'min': '50',
                'step': '10',
                'placeholder': '180'
            })
        }

    def clean_network_generations(self):
        # get list of received values
        selected = self.cleaned_data['network_generations']
        # combining via comma
        return ','.join(selected)



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
                'placeholder': 'Nitro S5',
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
