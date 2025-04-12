from django.shortcuts import HttpResponse
from myapp.services.db_service import DbService
from myapp.models import User


def test_sign_up(request):

    """
    Test method to sign up a new user
    :param request: Http request object
    :return: Http response object
    """
    email = request.GET.get('email')
    password = request.GET.get('password')
    new_user = DbService.sign_up(email=email, password=password)
    if isinstance(new_user, User):
        return HttpResponse(f"Користувача {new_user.email} успішно зареєстровано!")
    else:
        return HttpResponse(f"Помилка: {new_user}")

def test_sign_in(request):
    """
    Test method for signing in as an existing user
    :param request: Http request object
    :return: Http response object
    """
    email = request.GET.get('email')
    password = request.GET.get('password')
    user = DbService.sign_in(request, email=email, password=password)
    if user:
        return HttpResponse(f"Успішний вхід для {user.email}")
    else:
        return HttpResponse("Невірний email або пароль.")
