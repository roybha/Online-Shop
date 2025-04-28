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

    # path for adding products to the current cart
    path('cart/add/<int:product_id>',
         views.add_to_cart,
         name='add_to_cart'),

    # path for show current cart
    path('cart',
         views.show_cart,
         name='show_cart'),

    # path for confirming specific order
    path('cart/confirm/',
         views.confirm_order,
         name='confirm_order'
    ),

    # path for orders check by some buyer
    path('orders/list',
         views.list_user_orders,
         name='list_user_orders'),

    # path for deleting order
    path('orders/delete/<int:order_id>',
         views.delete_order,
         name='delete_order'),

    # path for deleting from cart
    path('cart/delete/<int:product_id>/',
         views.remove_from_cart,
         name='remove_from_cart'),

    # path for catalog of products
    path('',
         views.catalog,
         name='catalog'),

    # path for all unconfirmed orders page
    path('orders/status/',
         views.show_unconfirmed_orders,
         name='show_unconfirmed_orders'),

    # path for changing specified order's status
    path('orders/status/<int:order_id>/',
         views.status_change,
         name='status_change'),
]
