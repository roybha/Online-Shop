from . import views
from django.urls import path

urlpatterns = [

    # path for registration a new user
    path('sign-up', views.sign_up, name='sign_up'),

    # path for login as existing user
    path('sign-in', views.sign_in, name='sign_in'),

    # path fot log out from app
    path('log-out', views.log_out, name='log_out'),

    # path for add laptop to shop
    path('add_laptop', views.add_laptop_product, name='add_laptop_product'),
]
