from django.shortcuts import render, redirect
from myapp.services.db_service import DbService
from django.contrib.auth import logout, login
from django.contrib import messages
from myapp.models import User, Brand, Product
from .forms import LaptopForm, ProductForm, SmartphoneForm
from .models import Category


def sign_up(request):

    """
    Method to sign up a new user
    :param request: Http request object
    :return: sign up page
    """

    # check if both email and password
    # are provided in the POST request
    if (request.POST.get('email') is not None
            and request.POST.get('password') is not None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # check if passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords must match')
            return render(request, 'sign_up.html')

        # try to register the new user using the DbService
        new_user = DbService.sign_up(email=email, password=password)

        # if a valid User object is returned, registration is successful
        if isinstance(new_user, User):
            messages.info(
                request,
                f"Користувача {new_user.email} успішно зареєстровано!"
            )

            # return sign_in html form
            return render(request, 'sign_in.html')
        else:
            # handle registration failure
            messages.info(request, "Помилка авторизації")

            # return sign_up html form
            return render(request, 'sign_up.html')
    else:

        # if not a POST request or required fields are missing,
        # render the sign_up html form
        return render(request, 'sign_up.html')


def sign_in(request):
    """
    Method for signing in as an existing user
    :param request: Http request object
    :return: sign in page
    """

    # check if both email and password
    # are provided in the POST request
    if (request.POST.get('email') is not None
            and request.POST.get('password') is not None):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # try to authenticate user using the DbService
        user = DbService.sign_in(email, password)
        # if authentication succeeds,
        # redirect to dashboard with user cont
        if user is not None:
            login(request, user)
            request.session.save()
            return redirect('dashboard')
        else:

            # if authentication failed,
            # return back to sign-in page
            return render(request, 'sign_in.html')
    else:
        # if not a POST request or fields are missing,
        # render the sign-in form
        return render(request, 'sign_in.html')


def log_out(request):
    """
    Method of logging out from app
    :param request: Http request object
    :return: sign in page
    """
    # Call the embedded Django method for logging out
    logout(request)

    # Redirect on the sing in page after exit
    return redirect('dashboard')


def add_laptop_product(request):
    """
    Method for show  and also adding a new laptop to shop by seller
    :param request: Http request object
    :return: in case of correct adding redirect to success page
    else -> show the same page but with text message of exception
    """

    # if program use POST method for trying to add new laptop
    if request.method == 'POST':
        # get all entered data from forms
        laptop_form = LaptopForm(request.POST)
        product_form = ProductForm(request.POST)

        # if all entered data pass through validation checking -> save
        if laptop_form.is_valid() and product_form.is_valid():

            # get cpu's brand from laptop form
            cpu_brand_name = laptop_form.cleaned_data['cpu_brand_name']

            # get gpu's brand from laptop form
            gpu_brand_name = laptop_form.cleaned_data['gpu_brand_name']

            # get product's brand from product form
            brand_name = product_form.cleaned_data['brand_name']

            # get value of input field for cpu's brand
            cpu_brand, _ = Brand.objects.get_or_create(name=cpu_brand_name)

            # get value of input field for gpu's brand
            gpu_brand, _ = Brand.objects.get_or_create(name=gpu_brand_name)

            # get value of input field for product's brand
            product_brand, _ = Brand.objects.get_or_create(name=brand_name)

            # save values of laptop's form
            # but don't commit changes in db
            laptop = laptop_form.save(commit=False)

            # assign cpu's brand the value of
            # corresponding input field
            laptop.cpu_brand = cpu_brand

            # assign gpu's brand the value of
            # corresponding input field
            laptop.gpu_brand = gpu_brand

            # save laptop instance
            laptop.save()

            # create, but do not save the product object yet
            product = product_form.save(commit=False)

            # connect product's category id and category's own id
            product.category_prod_id = laptop.id

            # find the category object with
            # the name "laptop" and bind it to the product if exists
            # else create such category
            category, _ = Category.objects.get_or_create(name='laptop')

            # connect product's category id and category's own id
            product.category_id = category.id

            # assign product's brand the value of
            # corresponding input field
            product.brand = product_brand

            # store the finished product object in the database
            product.save()

            # successful addition - redirect to default page
            return redirect('add_laptop_product')

    # if the method is GET, we create empty forms to display on the page
    else:
        laptop_form = LaptopForm()
        product_form = ProductForm()

    # return an HTML page with both forms
    return render(
        request,
        'add_laptop.html',
        {
            'laptop_form': laptop_form,
            'product_form': product_form
        }
    )

def add_smartphone_product(request):
    """
    Method for show and also adding a new smartphone to shop by seller
    :param request: Http request object
    :return: in case of correct adding redirect to success page
    else -> show the same page but with text message of exception
    """

    # if program use POST method
    # for trying to add new smartphone
    if request.method == 'POST':

        # get all entered data from forms
        smartphone_form = SmartphoneForm(request.POST)
        product_form = ProductForm(request.POST)

        # if all entered data pass through validation checking -> save
        if smartphone_form.is_valid() and product_form.is_valid():

            # get entered network generations
            network_generations = smartphone_form.cleaned_data[
                'network_generations'
            ]

            # get entered brand name
            brand_name = product_form.cleaned_data[
                'brand_name'
            ]

            # get value of input field for product's brand
            product_brand, _ = Brand.objects.get_or_create(name=brand_name)

            # save values smartphone's form
            # but don't commit changes in db
            smartphone = smartphone_form.save(commit=False)

            # assign smartphone's network generations
            # value of corresponding input field
            smartphone.network_generations = network_generations

            # save smartphone in db
            smartphone.save()

            # create, but do not save the product object yet
            product = product_form.save(commit=False)

            # connect product's category id and category's own id
            product.category_prod_id = smartphone.id

            # find the category object with
            # the name "laptop" and bind it to the product if exists
            # else create such category
            category, _ = Category.objects.get_or_create(name='smartphone')

            # connect product's category id and category's own id
            product.category_id = category.id

            # assign product's brand the value of
            # corresponding input field
            product.brand = product_brand

            # store the finished product object in the database
            product.save()

            # successful addition - redirect to default page
            return redirect('add_smartphone_product')
    else:
        # if the method is GET, we create empty forms to display on the page
        smartphone_form = SmartphoneForm()
        product_form = ProductForm()

    # return an HTML page with both forms
    return render(
        request,
        'add_smartphone.html',
        {
            'smartphone_form': smartphone_form,
            'product_form': product_form
        }
    )

def get_all_products_by_category(request, category_name: str):
    """
    Method for getting all products by  specific category
    :param request: Http request object
    :param category_name: str in which category we want to get  all products
    :return: page of available products by category
    """

    # search specific category in correspond table
    category = Category.objects.get(name=category_name)

    # search products that represents this category
    products = Product.objects.filter(category=category.id)

    # choose the correct word for view's field
    category_for_view = 'ноутбуки' if category.name == 'laptop' else 'смартфони'
    return render(request,
                  'products_by_category.html',
                  {
                   'products': products,
                   'category_name': category_for_view
                   }
    )

def dashboard(request):
    """
    Method for showing user's panel
    :param request: Http request object
    :return: dashboard html page
    """
    return render(request, 'dashboard.html')
