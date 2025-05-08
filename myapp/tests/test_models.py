from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from myapp.models import User, Order, Category, Brand, Product, OrderItem, Laptop, \
    Smartphone
from myapp.services.credentials_service import CredentialsService
from datetime import date
from decimal import Decimal


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email=self.__class__.email,
                                             password=self.__class__.password,
                                             role=self.__class__.role)

    @classmethod
    def setUpTestData(cls):
        cls.email = "seller@gmail.com"
        cls.password = "password123"
        cls.role = "seller"

    def test_user_creation(self):
        user = self.user
        password = self.__class__.password
        self.assertEqual(user.email, "seller@gmail.com")
        self.assertTrue(CredentialsService.check_password(user.password, password))
        self.assertEqual(user.role, "seller")

    def test_default_values(self):
        user = self.user
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)

    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email=self.email, password="somepassword123",
                                     role="user")


class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(user=self.__class__.user,
                                          price=self.__class__.price)

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="some@email.com",
                                            password="password123", role="user")
        cls.price = 10000

    def test_order_creation(self):
        order = self.order
        self.assertEqual(order.user, self.__class__.user)
        self.assertEqual(order.price, self.__class__.price)

    def test_default_values(self):
        order = self.order
        self.assertEqual(order.status, False)
        self.assertEqual(order.order_date, date.today())

    def test_order_deletion_on_user_cascade(self):
        order = self.order
        user = order.user

        user.delete()  # delete the user

        self.assertEqual(Order.objects.count(), 0)  # check if order has been deleted


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = "laptop"

    def setUp(self):
        self.category = Category.objects.create(name=self.__class__.name)

    def test_category_creation(self):
        category = self.category
        name = self.__class__.name
        self.assertEqual(category.name, name)

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name=self.__class__.name)

    def test_category_str_method(self):
        category = self.category
        category_str = str(category)
        self.assertEqual(category_str, category.name)


class BrandModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.name = 'Asus'

    def setUp(self):
        self.brand = Brand.objects.create(name=self.__class__.name)

    def test_brand_creation(self):
        brand = self.brand
        self.assertEqual(brand.name, self.__class__.name)

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name=self.__class__.name)

    def test_brand_str_method(self):
        brand = self.brand
        brand_str = str(brand)
        self.assertEqual(brand_str, brand.name)


class LaptopModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.screen_size = Decimal("15.6")
        cls.screen_resolution = "1920x1080"
        cls.cpu_model = "i7-12700H"
        cls.cpu_frequency = Decimal("2.3")
        cls.ram_type = "DDR4"
        cls.storage_type = "SSD"
        cls.gpu_model = "RTX 3060"

    def setUp(self):
        self.cpu_brand = Brand.objects.create(name="Intel")
        self.gpu_brand = Brand.objects.create(name="NVIDIA")

        self.laptop = Laptop.objects.create(
            screen_size=self.__class__.screen_size,
            scree_resolution=self.__class__.screen_resolution,
            cpu_brand=self.cpu_brand,
            cpu_model=self.__class__.cpu_model,
            cpu_frequency=self.__class__.cpu_frequency,
            ram_type=self.__class__.ram_type,
            storage_type=self.__class__.storage_type,
            gpu_brand=self.gpu_brand,
            gpu_model=self.__class__.gpu_model
        )

    def test_laptop_creation(self):
        laptop = self.laptop
        self.assertEqual(laptop.screen_size, self.__class__.screen_size)
        self.assertEqual(laptop.scree_resolution, self.__class__.screen_resolution)
        self.assertEqual(laptop.cpu_brand, self.cpu_brand)
        self.assertEqual(laptop.cpu_model, self.__class__.cpu_model)
        self.assertEqual(laptop.cpu_frequency, self.__class__.cpu_frequency)
        self.assertEqual(laptop.ram_type, self.__class__.ram_type)
        self.assertEqual(laptop.storage_type, self.__class__.storage_type)
        self.assertEqual(laptop.gpu_brand, self.gpu_brand)
        self.assertEqual(laptop.gpu_model, self.__class__.gpu_model)

    def test_default_values(self):
        laptop = self.laptop
        self.assertEqual(laptop.screen_ref_rate, 60)
        self.assertEqual(laptop.cpu_cores_num, 4)
        self.assertEqual(laptop.ram, 4)
        self.assertEqual(laptop.storage, 120)

    def test_screen_resolution_validation(self):
        with self.assertRaises(ValidationError):
            invalid_laptop = Laptop(
                screen_size=Decimal("15.6"),
                scree_resolution="invalid",
                cpu_brand=self.cpu_brand,
                cpu_model="i7-12700H",
                cpu_frequency=Decimal("2.3"),
                ram_type="DDR4",
                storage_type="SSD",
                gpu_brand=self.gpu_brand,
                gpu_model="RTX 3060"
            )
            invalid_laptop.full_clean()

    def test_laptop_deletion_on_brand_cascade(self):
        self.assertEqual(Laptop.objects.count(), 1)

        self.cpu_brand.delete()

        self.assertEqual(Laptop.objects.count(), 0)


class SmartphoneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.screen_size = Decimal("6.5")
        cls.screen_resolution = "1920x1080"
        cls.network_generations = "5G"
        cls.cpu_model = "Snapdragon 888"
        cls.main_camera = "48MP"
        cls.max_video_resolution = "7680 x 4320 8K UHD"
        cls.frontal_camera = "12MP"
        cls.connector_type = "USB-C"

    def setUp(self):
        self.smartphone = Smartphone.objects.create(
            screen_size=self.__class__.screen_size,
            screen_resolution=self.__class__.screen_resolution,
            network_generations=self.__class__.network_generations,
            cpu_model=self.__class__.cpu_model,
            main_camera=self.__class__.main_camera,
            max_video_resolution=self.__class__.max_video_resolution,
            frontal_camera=self.__class__.frontal_camera,
            connector_type=self.__class__.connector_type
        )

    def test_smartphone_creation(self):
        smartphone = self.smartphone
        self.assertEqual(smartphone.screen_size, self.__class__.screen_size)
        self.assertEqual(smartphone.screen_resolution, self.__class__.screen_resolution)
        self.assertEqual(smartphone.network_generations,
                         self.__class__.network_generations)
        self.assertEqual(smartphone.cpu_model, self.__class__.cpu_model)
        self.assertEqual(smartphone.main_camera, self.__class__.main_camera)
        self.assertEqual(smartphone.max_video_resolution,
                         self.__class__.max_video_resolution)
        self.assertEqual(smartphone.frontal_camera, self.__class__.frontal_camera)
        self.assertEqual(smartphone.connector_type, self.__class__.connector_type)

    def test_default_values(self):
        smartphone = self.smartphone
        self.assertEqual(smartphone.screen_ref_rate, 60)
        self.assertEqual(smartphone.sim_quantity, 1)
        self.assertEqual(smartphone.cpu_cores_num, 8)
        self.assertEqual(smartphone.ram, 4)
        self.assertEqual(smartphone.storage, 120)
        self.assertEqual(smartphone.nfc, False)
        self.assertEqual(smartphone.battery, 2000)
        self.assertEqual(smartphone.weight, 200)

    def test_screen_resolution_validation(self):
        with self.assertRaises(ValidationError):
            invalid_smartphone = Smartphone(
                screen_size=Decimal("6.5"),
                screen_resolution="invalid",
                network_generations="5G",
                cpu_model="Snapdragon 888",
                main_camera="48MP",
                max_video_resolution="7680 x 4320 8K UHD",
                frontal_camera="12MP",
                connector_type="USB-C"
            )
            invalid_smartphone.full_clean()

    def test_max_video_resolution_validation(self):
        with self.assertRaises(ValidationError):
            invalid_smartphone = Smartphone(
                screen_size=Decimal("6.5"),
                screen_resolution="1920x1080",
                network_generations="5G",
                cpu_model="Snapdragon 888",
                main_camera="48MP",
                max_video_resolution="invalid",
                frontal_camera="12MP",
                connector_type="USB-C"
            )
            invalid_smartphone.full_clean()


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model_name = "Laptop Samsung Galaxy Book Pro"
        cls.description = "Nice lightweight laptop for work"
        cls.category = Category.objects.create(name="laptop")
        cls.category_prod_id = 1
        cls.brand = Brand.objects.create(name="Samsung")
        cls.price = 25000
        cls.image_url = "https://www.google.com/imgres?q=samsung%20laptop&imgurl"

    def setUp(self):
        self.product = Product.objects.create(model_name=self.__class__.model_name,
                                              description=self.__class__.description,
                                              category=self.__class__.category,
                                              category_prod_id=self.__class__.category_prod_id,
                                              brand=self.__class__.brand,
                                              price=self.__class__.price,
                                              image_url=self.__class__.image_url)

    def test_product_creation(self):
        product = self.product
        self.assertEqual(product.model_name, self.__class__.model_name)
        self.assertEqual(product.description, self.__class__.description)
        self.assertEqual(product.category, self.__class__.category)
        self.assertEqual(product.category_prod_id, self.__class__.category_prod_id)
        self.assertEqual(product.brand, self.__class__.brand)
        self.assertEqual(product.price, self.__class__.price)
        self.assertEqual(product.image_url, self.__class__.image_url)

    def test_product_deletion_on_category_cascade(self):
        category = self.__class__.category
        product = self.product

        category.delete()  # delete the category

        self.assertEqual(Product.objects.count(), 0)  # check if product was deleted


class OrderItemModelTest(TestCase):
    def setUp(self):
        dummy_user = User.objects.create_user(email="some@gmail.com",
                                              password="password123", role="user")
        self.order = Order.objects.create(user=dummy_user, price=1000)
        self.product = Product.objects.create(model_name="some model",
                                             description="any",
                                             category=Category.objects.create(
                                                 name="laptop"),
                                             category_prod_id=1,
                                             brand=Brand.objects.create(name="Apple"),
                                             price=Decimal(120000),
                                             image_url="https://some.com")
        self.order_item = OrderItem.objects.create(order=self.order,
                                                   product=self.product)

    def test_order_item_creation(self):
        order_item = self.order_item
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)

    def test_default_values(self):
        order_item = self.order_item
        self.assertEqual(order_item.quantity, 1)

    def test_order_item_deletion_on_order_cascade(self):
        order = self.order
        self.assertEqual(OrderItem.objects.count(), 1)

        order.delete()  # delete the order

        self.assertEqual(OrderItem.objects.count(), 0)

    def test_order_item_deletion_on_product_cascade(self):
        product = self.product
        self.assertEqual(OrderItem.objects.count(), 1)

        product.delete()

        self.assertEqual(OrderItem.objects.count(), 0)