from django.shortcuts import render, redirect
from myapp.services.db_service import DbService
from django.contrib.auth import logout
from django.contrib import messages
from myapp.models import User
from .forms import LaptopForm,ProductForm
from .models import Category


def test_sign_up(request):

    """
    Test method to sign up a new user
    :param request: Http request object
    :return: sign up page
    """
    if request.GET.get('email') is not None and request.GET.get('password') is not None:
        email = request.GET.get('email')
        password = request.GET.get('password')
        password_confirm = request.GET.get('password_confirm')
        if password != password_confirm:
            messages.error(request, 'Passwords must match')
            return render(request,'sign_up.html')
        new_user = DbService.sign_up(email=email, password=password)
        if isinstance(new_user, User):
            messages.info(request, f"Користувача {new_user.email} успішно зареєстровано!")
            return render(request, 'sign_in.html')
        else:
            messages.info(request, f"Помилка авторизації")
            return render(request, 'sign_up.html')
    else:
        return render(request, 'sign_up.html')

def test_sign_in(request):
    """
    Test method for signing in as an existing user
    :param request: Http request object
    :return: sign in page
    """
    if request.GET.get('email')is not None and request.GET.get('password') is not None:
        email = request.GET.get('email')
        password = request.GET.get('password')
        user = DbService.sign_in(request, email, password)
        if user is not None:
            return render(request, 'dashboard.html', {'user': user})
        else:
            return render(request, 'sign_in.html')
    else:
        return render(request,'sign_in.html')

def test_log_out(request):
    """
    Method of logging out from app
    :param request: Http request object
    :return: sign in page
    """
    # Call the embedded Django method for logging out
    logout(request)

    # Redirect on the sing in page after exit
    return redirect('test_sign_in')

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

            # save laptop instance
            laptop = laptop_form.save()

            # create, but do not save the product object yet
            product = product_form.save(commit=False)

            # assign the category_prod_id field the identifier of the newly saved laptop
            product.category_prod_id= laptop.id

            # find the category object with the name "laptop" and bind it to the product
            product.category = Category.objects.get(name='laptop')

            # store the finished product object in the database
            product.save()

            # successful addition - redirect to login/success page
            return redirect('test_sign_in')

    # if the method is GET, we create empty forms to display on the page
    else:
        laptop_form = LaptopForm()
        product_form = ProductForm()

    # return an HTML page with both forms
    return render(request, 'add_laptop.html', {'laptop_form': laptop_form, 'product_form': product_form})