from . import views
from django.urls import path

urlpatterns = [

    # path for registration a new user
    path('sign-up',
         views.sign_up,
         name='sign_up'
    ),

    # path for login as existing user
    path('sign-in',
         views.sign_in,
         name='sign_in'
    ),

    # path fot log out from app
    path('log-out',
         views.log_out,
         name='log_out'
    ),

    # path for add laptop to shop
    path('add_laptop',
         views.add_laptop_product,
         name='add_laptop_product'
    ),

    # path for add smartphone
    path('add_smartphone',
         views.add_smartphone_product,
         name='add_smartphone_product'
    ),

    # path for dashboard
    path('dashboard',
         views.dashboard,
         name='dashboard'
    ),

    # path for get all products by specific category
    path('products/<str:category_name>/',
         views.get_all_products_by_category,
         name='products_by_category'
    ),

    # path for details about specific product by name and category
    path('product/<str:product_category>/<str:product_name>/',
         views.product_detail,
         name='product_detail'
    ),

    path('cart/add/<int:product_id>',
         views.add_to_cart,
         name='add_to_cart'),

    path('cart/show',
         views.show_cart,
         name='show_cart'),

    path('cart/confirm/',
         views.confirm_order,
         name='confirm_order'
    ),
]
