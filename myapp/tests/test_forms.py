from django.test import TestCase
from django.core.exceptions import ValidationError
from myapp.forms import LaptopForm, SmartphoneForm, ProductForm
from myapp.models import Laptop, Brand
from decimal import Decimal


class LaptopFormTest(TestCase):
    def setUp(self):
        self.cpu_brand = Brand.objects.create(name="Intel")
        self.gpu_brand = Brand.objects.create(name="NVIDIA")

    def test_form_valid_data(self):
        form_data = {
            'screen_size': '15.6',
            'scree_resolution': '1920x1080',
            'screen_ref_rate': '120',
            'cpu_brand_name': 'Intel',
            'cpu_model': 'i7-12700H',
            'cpu_cores_num': '8',
            'cpu_frequency': '2.3',
            'ram': '16',
            'ram_type': 'DDR4',
            'storage': '500',
            'storage_type': 'SSD',
            'gpu_brand_name': 'NVIDIA',
            'gpu_model': 'RTX 3060'
        }
        form = LaptopForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['screen_size'], Decimal('15.6'))
        self.assertEqual(form.cleaned_data['scree_resolution'], '1920x1080')
        self.assertEqual(form.cleaned_data['screen_ref_rate'], 120)
        self.assertEqual(form.cleaned_data['cpu_brand_name'], 'Intel')
        self.assertEqual(form.cleaned_data['cpu_model'], 'i7-12700H')
        self.assertEqual(form.cleaned_data['cpu_cores_num'], 8)
        self.assertEqual(form.cleaned_data['cpu_frequency'], Decimal('2.3'))
        self.assertEqual(form.cleaned_data['ram'], 16)
        self.assertEqual(form.cleaned_data['ram_type'], 'DDR4')
        self.assertEqual(form.cleaned_data['storage'], 500)
        self.assertEqual(form.cleaned_data['storage_type'], 'SSD')
        self.assertEqual(form.cleaned_data['gpu_brand_name'], 'NVIDIA')
        self.assertEqual(form.cleaned_data['gpu_model'], 'RTX 3060')

    def test_form_invalid_resolution(self):
        form_data = {
            'screen_size': '15.6',
            'scree_resolution': 'invalid',
            'screen_ref_rate': '120',
            'cpu_brand_name': 'Intel',
            'cpu_model': 'i7-12700H',
            'cpu_cores_num': '8',
            'cpu_frequency': '2.3',
            'ram': '16',
            'ram_type': 'DDR4',
            'storage': '500',
            'storage_type': 'SSD',
            'gpu_brand_name': 'NVIDIA',
            'gpu_model': 'RTX 3060'
        }
        form = LaptopForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('scree_resolution', form.errors)

    def test_form_invalid_brand(self):
        form_data = {
            'screen_size': '15.6',
            'scree_resolution': '1920x1080',
            'screen_ref_rate': '120',
            'cpu_brand_name': 'NonExistentBrand',
            'cpu_model': 'i7-12700H',
            'cpu_cores_num': '8',
            'cpu_frequency': '2.3',
            'ram': '16',
            'ram_type': 'DDR4',
            'storage': '500',
            'storage_type': 'SSD',
            'gpu_brand_name': 'NonExistentBrand',
            'gpu_model': 'RTX 3060'
        }
        form = LaptopForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['cpu_brand_name'], 'NonExistentBrand')
        self.assertEqual(form.cleaned_data['gpu_brand_name'], 'NonExistentBrand')

    def test_form_field_attributes(self):
        form = LaptopForm()
        self.assertEqual(form.fields['screen_size'].widget.attrs['step'], '0.1')
        self.assertEqual(form.fields['screen_size'].widget.attrs['placeholder'], '13.3')
        self.assertEqual(form.fields['screen_size'].widget.attrs['max'], '90')
        self.assertEqual(form.fields['scree_resolution'].widget.attrs['pattern'],
                         r'^\d{3,4}x\d{3,4}$')
        self.assertEqual(form.fields['screen_ref_rate'].widget.attrs['min'], '60')
        self.assertEqual(form.fields['screen_ref_rate'].widget.attrs['max'], '240')
        self.assertEqual(form.fields['cpu_cores_num'].widget.attrs['min'], '2')
        self.assertEqual(form.fields['cpu_cores_num'].widget.attrs['max'], '20')
        self.assertEqual(form.fields['cpu_frequency'].widget.attrs['max'], '40')
        self.assertEqual(form.fields['ram'].widget.attrs['step'], '2')
        self.assertEqual(form.fields['ram'].widget.attrs['max'], '40')
        self.assertEqual(form.fields['storage'].widget.attrs['step'], '10')
        self.assertEqual(form.fields['storage'].widget.attrs['min'], '120')
        self.assertEqual(form.fields['storage'].widget.attrs['max'], '2000')


class SmartphoneFormTest(TestCase):
    def test_form_valid_data(self):
        # Test form with valid data
        form_data = {
            'screen_size': '6.5',
            'screen_resolution': '1920x1080',
            'screen_ref_rate': '120',
            'sim_quantity': '2',
            'network_generations': ['4G', '5G'],
            'cpu_model': 'Snapdragon 888',
            'cpu_cores_num': '8',
            'ram': '6',
            'storage': '128',
            'main_camera': '48+12',
            'max_video_resolution': '7680 x 4320 8K UHD',
            'frontal_camera': '12',
            'nfc': True,
            'connector_type': 'USB-C',
            'battery': '4000',
            'weight': '180'
        }
        form = SmartphoneForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Check cleaned data, including custom cleaning of network_generations
        self.assertEqual(form.cleaned_data['network_generations'], '4G,5G')

        # Save and verify the instance
        smartphone = form.save()
        self.assertEqual(smartphone.screen_size, Decimal('6.5'))
        self.assertEqual(smartphone.screen_resolution, '1920x1080')
        self.assertEqual(smartphone.screen_ref_rate, 120)
        self.assertEqual(smartphone.sim_quantity, 2)
        self.assertEqual(smartphone.network_generations, '4G,5G')
        self.assertEqual(smartphone.cpu_model, 'Snapdragon 888')
        self.assertEqual(smartphone.cpu_cores_num, 8)
        self.assertEqual(smartphone.ram, 6)
        self.assertEqual(smartphone.storage, 128)
        self.assertEqual(smartphone.main_camera, '48+12')
        self.assertEqual(smartphone.max_video_resolution, '7680 x 4320 8K UHD')
        self.assertEqual(smartphone.frontal_camera, '12')
        self.assertTrue(smartphone.nfc)
        self.assertEqual(smartphone.connector_type, 'USB-C')
        self.assertEqual(smartphone.battery, 4000)
        self.assertEqual(smartphone.weight, 180)

    def test_form_invalid_resolution(self):
        # Test invalid screen resolution
        form_data = {
            'screen_size': '6.5',
            'screen_resolution': 'invalid',
            'screen_ref_rate': '120',
            'sim_quantity': '2',
            'network_generations': ['4G', '5G'],
            'cpu_model': 'Snapdragon 888',
            'cpu_cores_num': '8',
            'ram': '6',
            'storage': '128',
            'main_camera': '48+12',
            'max_video_resolution': '7680 x 4320 8K UHD',
            'frontal_camera': '12',
            'nfc': True,
            'connector_type': 'USB-C',
            'battery': '4000',
            'weight': '180'
        }
        form = SmartphoneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('screen_resolution', form.errors)

    def test_form_invalid_max_video_resolution(self):
        # Test invalid max video resolution
        form_data = {
            'screen_size': '6.5',
            'screen_resolution': '1920x1080',
            'screen_ref_rate': '120',
            'sim_quantity': '2',
            'network_generations': ['4G', '5G'],
            'cpu_model': 'Snapdragon 888',
            'cpu_cores_num': '8',
            'ram': '6',
            'storage': '128',
            'main_camera': '48+12',
            'max_video_resolution': 'invalid',
            'frontal_camera': '12',
            'nfc': True,
            'connector_type': 'USB-C',
            'battery': '4000',
            'weight': '180'
        }
        form = SmartphoneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('max_video_resolution', form.errors)

    def test_form_invalid_network_generations(self):
        form_data = {
            'screen_size': '6.5',
            'screen_resolution': '1920x1080',
            'screen_ref_rate': '120',
            'sim_quantity': '2',
            'network_generations': ['6G'],  # invalid choice
            'cpu_model': 'Snapdragon 888',
            'cpu_cores_num': '8',
            'ram': '6',
            'storage': '128',
            'main_camera': '48+12',
            'max_video_resolution': '7680 x 4320 8K UHD',
            'frontal_camera': '12',
            'nfc': True,
            'connector_type': 'USB-C',
            'battery': '4000',
            'weight': '180'
        }
        form = SmartphoneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('network_generations', form.errors)

    def test_form_field_attributes(self):
        form = SmartphoneForm()
        self.assertEqual(form.fields['screen_size'].widget.attrs['step'], '0.1')
        self.assertEqual(form.fields['screen_size'].widget.attrs['placeholder'], '4.3')
        self.assertEqual(form.fields['screen_size'].widget.attrs['max'], '10')
        self.assertEqual(form.fields['screen_ref_rate'].widget.attrs['min'], '60')
        self.assertEqual(form.fields['screen_ref_rate'].widget.attrs['max'], '240')
        self.assertEqual(form.fields['sim_quantity'].widget.attrs['min'], '1')
        self.assertEqual(form.fields['sim_quantity'].widget.attrs['max'], '3')
        self.assertEqual(form.fields['cpu_cores_num'].widget.attrs['min'], '4')
        self.assertEqual(form.fields['cpu_cores_num'].widget.attrs['max'], '12')
        self.assertEqual(form.fields['ram'].widget.attrs['min'], '2')
        self.assertEqual(form.fields['ram'].widget.attrs['max'], '12')
        self.assertEqual(form.fields['storage'].widget.attrs['min'], '64')
        self.assertEqual(form.fields['storage'].widget.attrs['max'], '256')
        self.assertEqual(form.fields['main_camera'].widget.attrs['pattern'],
                         r'^(\d+\+)*\d+$')
        self.assertEqual(form.fields['max_video_resolution'].widget.attrs['pattern'],
                         r'^\d{3,5}\sx\s\d{3,5}(?:\s[\w\s]{2,15})?$')
        self.assertEqual(form.fields['frontal_camera'].widget.attrs['pattern'],
                         r'^\d+$')
        self.assertEqual(form.fields['battery'].widget.attrs['min'], '500')
        self.assertEqual(form.fields['battery'].widget.attrs['max'], '6500')
        self.assertEqual(form.fields['weight'].widget.attrs['placeholder'], '180')


class ProductFormTest(TestCase):
    def setUp(self):
        # Create a Brand instance for testing (though not used in form directly)
        self.brand = Brand.objects.create(name="Acer")

    def test_form_valid_data(self):
        # Test form with valid data, but don't save due to missing brand handling
        form_data = {
            'model_name': 'Nitro S5',
            'description': 'A powerful gaming laptop',
            'price': '75000.50',
            'image_url': 'https://example.com/image.jpg',
            'brand_name': 'Acer'
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Check cleaned data
        self.assertEqual(form.cleaned_data['model_name'], 'Nitro S5')
        self.assertEqual(form.cleaned_data['description'], 'A powerful gaming laptop')
        self.assertEqual(form.cleaned_data['price'], Decimal('75000.50'))
        self.assertEqual(form.cleaned_data['image_url'],
                         'https://example.com/image.jpg')
        self.assertEqual(form.cleaned_data['brand_name'], 'Acer')

    def test_form_invalid_price(self):
        # Test invalid price (below minimum)
        form_data = {
            'model_name': 'Nitro S5',
            'description': 'A powerful gaming laptop',
            'price': '4000',  # Below min of 5000
            'image_url': 'https://example.com/image.jpg',
            'brand_name': 'Acer'
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())  # Price value is validated on the client side
        self.assertNotIn('price', form.errors)  # no error for price

    def test_form_invalid_image_url(self):
        # Test invalid image URL
        form_data = {
            'model_name': 'Nitro S5',
            'description': 'A powerful gaming laptop',
            'price': '75000.50',
            'image_url': 'not-a-url',  # Invalid URL format
            'brand_name': 'Acer'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('image_url', form.errors)

    def test_form_missing_required_field(self):
        # Test missing required field (model_name)
        form_data = {
            'description': 'A powerful gaming laptop',
            'price': '75000.50',
            'image_url': 'https://example.com/image.jpg',
            'brand_name': 'Acer'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('model_name', form.errors)

    def test_form_field_attributes(self):
        # Test field widget attributes
        form = ProductForm()
        self.assertEqual(form.fields['model_name'].widget.attrs['placeholder'],
                         'Nitro S5')
        self.assertEqual(form.fields['model_name'].widget.attrs['maxlength'], '50')
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)
        self.assertEqual(form.fields['description'].widget.attrs['placeholder'],
                         'Опис моделі...')
        self.assertEqual(form.fields['price'].widget.attrs['step'], '0.01')
        self.assertEqual(form.fields['price'].widget.attrs['min'], '5000')
        self.assertEqual(form.fields['price'].widget.attrs['max'], '120000')
        self.assertEqual(form.fields['image_url'].widget.attrs['placeholder'],
                         'https://example.com/image.jpg')
        self.assertEqual(form.fields['brand_name'].widget.attrs['placeholder'], 'Acer')
        self.assertEqual(form.fields['brand_name'].widget.attrs['maxlength'], '50')
