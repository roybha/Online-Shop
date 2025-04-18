from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from decimal import Decimal
from datetime import date
from myapp.services.managers.user_manager import UserManager


class User(AbstractUser):
    """
    Class that represents a table structure of users in database
    """

    # autoincrement id for record
    id = models.AutoField(primary_key=True)

    # user's email for additional identification
    email = models.EmailField(unique=True)

    # user's password
    password = models.CharField(max_length=100)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('seller', 'Seller')
    ]

    # user's role limited by admin and user
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    # required field for creating/operating as admin
    is_active = models.BooleanField(default=True)

    # required field for creating/operating as admin
    is_staff = models.BooleanField(default=False)

    # user's last date of login
    last_login = models.DateTimeField(null=True, blank=True)

    # necessary specification for
    # django's AbstractBaseUser identification through UserManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # connection of custom UserManager for authorization
    objects = UserManager()

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'users'


class Order(models.Model):
    """
    Class that represents a table structure of orders in database
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # FK that connect a specific User and Orders made through it's account
    user: int = models.ForeignKey(User, on_delete=models.CASCADE)

    # general price of whole order(sum of prices of it's parts)
    price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # status of order
    status: bool = models.BooleanField(default=False)

    # date of placing an order
    order_date: date = models.DateField(default=date.today)

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'orders'


class Category(models.Model):
    """
    Class that represents a table structure of products' categories in database
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)
    NAME_CHOICES = [
        ('laptop', 'Laptop'),
        ('smartphone', 'Smartphone'),
    ]

    # name of specific category of products
    name: str = models.CharField(
        max_length=20,
        unique=True,
        choices=NAME_CHOICES
    )

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Class that represents a table structure of products' brands in database'
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # name of a specific brand
    name: str = models.CharField(max_length=15, unique=True)

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'brands'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Class that represents a table structure of products in database
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # specific name of product's model
    model_name: str = models.CharField(max_length=50)

    # short description of a specific product
    description: str = models.TextField()

    # FK that connect specific product
    # with specific category of products(name of specific table)
    category: int = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    # identifier within specified table
    category_prod_id: int = models.IntegerField()

    # FK that connect product with specific brand
    brand: int = models.ForeignKey(Brand, on_delete=models.CASCADE)

    # price of product
    price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # url for image product
    image_url: str = models.URLField()

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'products'


class OrderItem(models.Model):
    """
    Class that represents a table structure of orders' items in database
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # FK that connect some order item with its whole
    order: int = models.ForeignKey(Order, on_delete=models.CASCADE)

    # FK that connect item of order with specific product
    product: int = models.ForeignKey(Product, on_delete=models.CASCADE)

    # quantity of specific products in order
    quantity: int = models.IntegerField(default=1)

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'order_items'


class Laptop(models.Model):
    """
    Class that represents a table structure of products of laptop type in db
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # diagonal screen size in inches
    screen_size: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # screen resolution in pixels
    scree_resolution: str = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}x\d{3,4}$',
                message='Формат має бути як 1920x1080'
            )
        ]
    )

    # reference rate of screen in hertz
    screen_ref_rate: int = models.IntegerField(default=60)

    # FK that represents brand of laptop's cpu
    cpu_brand: int = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='cpu_brand'
    )

    # name of laptop's CPU model
    cpu_model: str = models.CharField(max_length=15)

    # quantity of cores inside the CPU
    cpu_cores_num: int = models.IntegerField(default=4)

    # frequency of CPU in gigahertz
    cpu_frequency: Decimal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # volume of laptop's RAM
    ram: int = models.IntegerField(default=4)

    # type of RAM
    ram_type: str = models.CharField(max_length=5)

    # volume of laptop's main storage in gigabytes
    storage: int = models.IntegerField(default=120)

    # type of main storage
    storage_type: str = models.CharField(max_length=5)

    # FK that represent brand of laptop's GPU
    gpu_brand: int = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='gpu_brand'
    )

    # name of laptop's gpu model
    gpu_model: str = models.CharField(max_length=15)

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'laptops'


class Smartphone(models.Model):
    """
    Class that represents a table structure
    of products of smartphone type in db
    """

    # specific autoincrement id for record
    id: int = models.AutoField(primary_key=True)

    # diagonal screen size in inches
    screen_size: Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # screen resolution in pixels
    screen_resolution: str = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{3,4}x\d{3,4}$',
                message="Формат має бути як 1920x1080"
            )
        ]
    )

    # reference rate of screen in hertz
    screen_ref_rate: int = models.IntegerField(default=60)

    # quantity of sim slots in smartphone
    sim_quantity: int = models.IntegerField(default=1)

    # supported connection type
    network_generations: str = models.CharField(max_length=20)

    # name of smartphone's CPU model
    cpu_model: str = models.CharField(max_length=15)

    # quantity of cores inside smartphone CPU
    cpu_cores_num: int = models.IntegerField(default=8)

    # volume of smartphone's RAM
    ram: int = models.IntegerField(default=4)

    # volume of smartphone's main storage
    storage: int = models.IntegerField(default=120)

    # main camera resolution in megapixels
    main_camera: str = models.CharField(max_length=30)

    # max video resolution that are supported
    max_video_resolution: str = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^\d{3,5}\sx\s\d{3,5}(?:\s[\w\s]{2,15})?$',
                message='Формат має бути як "7680 x 4320" '
                        'або "7680 x 4320 8K UHD"'
            )
        ]
    )

    # frontal camera resolution in megapixels
    frontal_camera: str = models.CharField(max_length=30)

    # indicator that show NFC support by smartphone
    nfc: bool = models.BooleanField(default=False)

    # type of connection slot for charging
    connector_type: str = models.CharField(max_length=10)

    # capacity of battery in milli ampere per hour
    battery: int = models.IntegerField(default=2000)

    # weight of smartphone in grams
    weight: int = models.IntegerField(default=200)

    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'smartphones'
