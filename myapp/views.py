from django.shortcuts import render, redirect
from myapp.services.db_service import DbService
from django.contrib.auth import logout
from django.contrib import messages
from myapp.models import User


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
