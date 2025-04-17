from django.shortcuts import render, redirect
from myapp.services.db_service import DbService
from django.contrib.auth import logout, login
from django.contrib import messages
from myapp.models import User
from .forms import LaptopForm, ProductForm
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

            # save laptop instance
            laptop = laptop_form.save()

            # create, but do not save the product object yet
            product = product_form.save(commit=False)

            # assign the category_prod_id field
            # the identifier of the newly saved laptop
            product.category_prod_id = laptop.id

            # find the category object with
            # the name "laptop" and bind it to the product
            product.category = Category.objects.get(name='laptop')

            # store the finished product object in the database
            product.save()

            # successful addition - redirect to login/success page
            return redirect('sign_in')

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

def dashboard(request):
    return render(request, 'dashboard.html')
