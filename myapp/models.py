from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from decimal import Decimal
from datetime import date
from myapp.services.managers.user_manager import UserManager


class User(AbstractBaseUser):
    """
    Class that represents a table structure of users in database
    """

    # autoincrement id for record
    id : int = models.AutoField(primary_key=True)

    # user's email for additional identification
    email : str = models.CharField(max_length=40)

    # user's password
    password : str = models.CharField(max_length=100)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    # user's role limited by admin and user
    role : str = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # user's last date of login
    last_login = models.DateTimeField(null=True, blank=True)

    # necessary specification for django's AbstractBaseUser identification through UserManager
    USERNAME_FIELD = 'email'

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
    id : int = models.AutoField(primary_key=True)

    # FK that connect a specific User and Orders made through it's account
    user : int = models.ForeignKey(User, on_delete=models.CASCADE)

    # general price of whole order(sum of prices of it's parts)
    price : Decimal = models.DecimalField(max_digits=10, decimal_places=2)

    # status of order
    status : bool = models.BooleanField(default=False)

    # date of placing an order
    order_date : date = models.DateField(default=date.today)
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
    id : int = models.AutoField(primary_key=True)
    NAME_CHOICES = [
        ('laptop', 'Laptop'),
        ('smartphone', 'Smartphone'),
    ]

    # name of specific category of products
    name : str = models.CharField(max_length=20, unique=True,choices=NAME_CHOICES)
    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'categories'


class Brand(models.Model):
    """
    Class that represents a table structure of products' brands in database'
    """

    # specific autoincrement id for record
    id : int = models.AutoField(primary_key=True)

    # name of a specific brand
    name : str = models.CharField(max_length=15, unique=True)
    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'brands'


class Product(models.Model):
    """
    Class that represents a table structure of products in database
    """

    # specific autoincrement id for record
    id : int = models.AutoField(primary_key=True)

    # specific name of product's model
    model_name : str = models.CharField(max_length=50)

    # short description of a specific product
    description : str = models.TextField()

    # FK that connect specific product with specific category of products(name of specific table)
    category : int = models.ForeignKey(Category, on_delete=models.CASCADE)

    # identificator within specified table
    category_prod_id : int = models.IntegerField()

    # FK that connect product with specific brand
    brand: int = models.ForeignKey(Brand, on_delete=models.CASCADE)

    # price of product
    price: Decimal = models.DecimalField(max_digits=10, decimal_places=2)
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
    id : int = models.AutoField(primary_key=True)

    # FK that connect some order item with its whole
    order : int = models.ForeignKey(Order, on_delete=models.CASCADE)

    # FK that connect item of order with specific product
    product : int = models.ForeignKey(Product, on_delete=models.CASCADE)

    # quantity of specific products in order
    quantity : int = models.IntegerField(default=1)
    class Meta:
        """
        Internal class for additional setting of table
        """

        # specification of table's name
        db_table = 'order_items'
