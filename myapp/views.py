from django.shortcuts import render, redirect
from myapp.services.db_service import DbService
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import (User, Brand, Product, Category,
                          Laptop, Smartphone, Order, OrderItem)
from django.db.models import Min, Max
from .forms import LaptopForm, ProductForm, SmartphoneForm


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

            # check if 'next' parameter is in the request
            maybe_next = request.POST.get('next', None)  # None if no 'next'
            url = '/sign-in' if maybe_next is None else f'/sign-in?next={maybe_next}'
            # return sign_in html form with/without 'next' parameter
            return redirect(url)
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
            # Get the next parameter if it exists
            next_url = request.POST.get('next', 'dashboard')
            return redirect(next_url)
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

            # set custom model name
            product.model_name = f'Ноутбук {product_brand.name} {product_form.cleaned_data.get('model_name')}'

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

            # set custom model name
            product.model_name = f'Смартфон {product_brand.name} {product_form.cleaned_data.get('model_name')}'

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

def product_detail(request, product_category: str, product_name: str):
    """
    Method for showing details of specific product
    :param request: Http request object
    :param product_category: str which specify product's category
    :param product_name: str which specify product's name
    :return: html page with details of specific product by its category
    """

    # find category which connected to our product
    category = Category.objects.get(name=product_category)

    # find specific product which has such category and name
    product = Product.objects.get(category=category.id, model_name=product_name)

    # variable that will store details of specific product
    # depending on category
    extra_info = None

    # if category is laptop -> search in table Laptops
    if category.name.lower() == 'laptop':
        extra_info = Laptop.objects.get(id=product.category_prod_id)

    # if category is smartphone -> search in table Smartphones
    elif category.name.lower() == 'smartphone':
        extra_info = Smartphone.objects.get(id=product.category_prod_id)

    # return html page with details of specific product
    return render(request, 'product_detail.html', {
        'product': product,
        'extra_info': extra_info,
    })

def add_to_cart(request, product_id):
    """
    Method for adding product to cart
    :param request: Http request object
    :param product_id: specific product id
    that will be added to the cart
    :return: current cart
    """
    # get the current cart from the session
    # or create an empty one if it doesn't already exist
    cart = request.session.get('cart', {})

    # if the product is already in the cart
    if str(product_id) in cart:

        # increase its quantity by 1
        cart[str(product_id)] += 1
    else:

        # otherwise add it with a quantity of 1
        cart[str(product_id)] = 1

    # save the updated cart in the session
    request.session['cart'] = cart

    # redirect the user to the page
    # where adding has been called
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)


def show_cart(request):
    """
    Method for showing cart's items
    :param request: Http request object
    :return: html page with cart's items
    """
    # get the cart from the session (keys are string IDs of products)
    cart = request.session.get('cart', {})

    # we select all the products in the cart
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []

    # form a list of cart items for display
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],  # quantity from session
            'total': product.price * cart[str(product.id)]  # common price of product
        })

    # calculating common price of potential order
    total_price = sum(item['total'] for item in cart_items)

    # render cart html page with its items
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def remove_from_cart(request, product_id):
    """
    Method for removing a product from the cart.
    :param request: Http request object
    :param product_id: id of the specific product to remove
    :return: redirect to the updated cart page
    """
    # get the current cart from the session (cart is a dictionary where keys are product IDs)
    cart = request.session.get('cart', {})

    # check if the product exists in the cart
    if str(product_id) in cart:
        # delete the product from the cart
        del cart[str(product_id)]
        # save the updated cart to the session
        request.session['cart'] = cart
        messages.success(request, 'Товар успішно видалено з кошика.')
    else:
        # if the product is not in the cart
        messages.error(request, 'Товар не знайдено в кошику.')

    # redirect to the cart page to show the updated cart
    return redirect('show_cart')

def get_order_user(request):
    """
    Method that returns the user,
    or None with an error if the guest email is invalid
    :param request: Http request object
    :return: user if authenticated
    or redirect to sign_in page
    """

    # if user is authenticated
    if request.user.is_authenticated:

        # get him from request attribute
        return request.user

    # return None otherwise
    return None

def parse_cart_from_post(post_data):
    """
    Method for parsing the cart from post data.
    :param post_data: POST data containing product information
    :return: a dictionary representing the cart with product ids and quantities
    """

    # create a variable that will
    # represent user's cart
    new_cart = {}

    # parsing products from the post data
    for key, val in post_data.items():

        # skip keys that do not start with 'product_'
        if not key.startswith('product_'):
            continue

        # extract product id from the key (e.g. 'product_1' → '1')
        prod_id = key.split('_', 1)[1]
        try:

            # try to convert the value to an integer (quantity)
            qty = int(val)
        except (ValueError, TypeError):

            # skip the product if the quantity is not valid
            continue

        # add product to the cart if the quantity is greater than 0
        if qty > 0:
            new_cart[prod_id] = qty

    # return the parsed cart dictionary
    return new_cart

def create_order(user, cart):
    """
    Method for creating order and its items
    :param user: user that making an order
    :param cart: cart that consist of different products
    :return: created order with its items
    """

    #  create new order record into db
    order = Order.objects.create(user=user, price=0)

    # set initial total price
    total = 0

    # calculating total price by using quantity
    for prod_id, quantity in cart.items():
        product = Product.objects.get(id=prod_id)
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        total += product.price * quantity

    # set price of order after calculations
    order.price = total

    # save new order into db
    order.save()

    # return created order
    return order

def confirm_order(request):
    """
    Method for confirming order by clients
    :param request: Http request object
    :return: redirect to dashboard or show_cart
    """

    # if the request method is not POST, redirect to the show_cart page
    if request.method != 'POST':
        return redirect('show_cart')

    # 1) get the user of order
    user = get_order_user(request)

    # if user is not authenticated, redirect to sign-in page with the referer
    if not user:
        referer = '/cart/show'

        # here, we are redirecting to 'sign_in' with the `next` parameter
        return redirect(f'/sign-in?next={referer}')

    # 2) read and validate the new cart
    new_cart = parse_cart_from_post(request.POST)

    # if the cart is empty, show an error and return to show_cart
    if not new_cart:
        messages.error(request, 'Корзина порожня.')
        return redirect('show_cart')

    # save the updated cart to the session
    request.session['cart'] = new_cart

    # 3) create the order using the user and cart data
    create_order(user, new_cart)

    # 4) clear the cart in the session and redirect to the dashboard
    request.session['cart'] = {}
    return redirect('dashboard')

@login_required
def list_user_orders(request):
    """
    Method that returns all orders of current user
    :param request: Http request object
    :return: html-page with list of orders
    """

    # get current user from request attribute
    user = request.user

    # get all user's orders sorted by date
    orders = Order.objects.filter(user=user).order_by('order_date')

    # add to every order its items from OrderItem's table
    orders_with_items = []
    for order in orders:
        items = OrderItem.objects.filter(order_id=order.id).select_related('product')
        total_price = sum(item.product.price * item.quantity for item in items)
        orders_with_items.append({
            'order': order,
            'items': items,
            'total_price': total_price,
        })

    # return html page with collected orders
    return render(request, 'orders.html', {
        'orders_with_items': orders_with_items,
    })

@login_required
def delete_order(request, order_id):
    """
    Method for deleting an order
    :param request: Http request object
    :param order_id: specified order's id
    :return: updated list of orders of specified user
    """

    # search in Order table order
    # with this id
    order = Order.objects.get(id=order_id)

    # if order's creator isn't this user
    # -> return the same page with error message
    if request.user != order.user:
        messages.error(request,'Ви не маєте прпво видалити це замовлення')
    else:
        # if order's creator is this user
        # -> delete order, its items
        order_items = OrderItem.objects.filter(order_id=order_id)
        order_items.delete()
        order.delete()

    # redirect to the page of user's orders
    return redirect('list_user_orders')

def catalog(request):
    """
    Method for show catalog of products
    :param request: Http request object
    :return: html-page with list of products
    with potential filters
    """

    # find all products into db
    products = Product.objects.all()

    # get all filters by GET-params
    brand_filter = request.GET.getlist('brand')
    price_max = request.GET.get('price')
    selected_category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    # filtration by brand
    if brand_filter:
        products = products.filter(brand__name__in=brand_filter)

    # filtration by max price
    if price_max:
        products = products.filter(price__lte=price_max)

    # filtration by category
    # default -> None
    category = None
    if selected_category_id:
        products = products.filter(category__id=selected_category_id)
        try:
            category = Category.objects.get(id=selected_category_id)
        except Category.DoesNotExist:
            category = None

    # filtration by search query
    if search_query:
        products = products.filter(model_name__icontains=search_query)

    # setting(updating) min and max price
    price_stats = Product.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    min_price = price_stats['min_price'] or 0
    max_price = price_stats['max_price'] or 100000

    # filtration by selected price
    selected_price = request.GET.get('price')
    if selected_price:
        products = products.filter(price__lte=selected_price)

    # set all data into html-variables
    context = {
        'products': products,
        'brands': Product.objects.values_list('brand__name', flat=True).distinct(),
        'categories': formatted_categories(),
        'selected_brands': brand_filter,
        'selected_price': selected_price,
        'selected_category_id': selected_category_id,
        'category': category,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
    }

    # return html-catalog page
    return render(request, 'catalog.html', context)

def formatted_categories():
    """
    Method that returns a list of all available categories
    :return: str list of all available categories
    """
    formatted_categories = []
    for cat in Category.objects.all():
        formatted_name = 'Ноутбуки' if cat.name == 'laptop' else 'Смартфони' if cat.name == 'smartphone' else cat.name.title()
        formatted_categories.append({'id': cat.id, 'name': formatted_name})
    return formatted_categories

@login_required
def show_unconfirmed_orders(request):
    """
    Method that show confirmed orders for seller
    :param request: Http request object
    :return: html-page with non-ocnfirmed orders
    """

    # check user's role
    user: User = request.user
    if user.role == 'seller':

        # collect unconfirmed orders sorted by date
        unconfirmed_orders = Order.objects.filter(status=False).order_by('-order_date')
        return render(request, 'seller_orders.html', {'orders': unconfirmed_orders})
    else:

        # return message with error
        messages.error(request, 'У вас немає доступу до цієї сторінки.')
        return redirect('dashboard')


@login_required
def status_change(request, order_id):
    """
    Method that change status of order
    with specified id
    :param request: Http request object
    :param order_id: specified order's id
    :return: updated html-page with list of orders
    """
    user: User = request.user
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        if user.role == 'seller':
            if order.status:
                messages.info(request, 'Це замовлення вже підтверджено.')
            else:

                # if order's status is False
                # -> change it
                order.status = True
                order.save()
                messages.success(request, f'Замовлення №{order.id} підтверджено.')
        else:
            messages.error(request, 'У вас немає прав для підтвердження замовлень.')

    return redirect('show_unconfirmed_orders')  # повертаємося назад до списку


