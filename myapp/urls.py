from . import views
from django.urls import path

urlpatterns = [

    # path for registration a new user
    path('sign-up', views.test_sign_up, name='test_sign_up'),

    # path for login as existing user
    path('sign-in', views.test_sign_in, name='test_sign_in'),

    # path fot log out from app
    path('log-out', views.test_log_out, name='test_log_out'),
]