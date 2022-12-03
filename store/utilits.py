import json
from .models import *


def cookie_cart(request):
    try:
        cart_ = json.loads(request.COOKIES['cart'])
    except:
        cart_ = {}

    items = []
    order = {'get_items_price_total': 0, 'get_cart_items_total': 0, 'shipping': False}
    cart_item = order['get_cart_items_total']

    for i in cart_:
        try:
            cart_item += int(cart_[i]['quantity'])

            product = Product.objects.get(id=i)
            total = product.price * cart_[i]['quantity']

            order['get_cart_items_total'] += cart_[i]['quantity']
            order['get_items_price_total'] += total

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart_[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'cartItems': cart_item, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item = order.get_cart_items_total
    else:
        cookieCart = cookie_cart(request)
        order = cookieCart['order']
        cart_item = cookieCart['cartItems']
        items = cookieCart['items']
    return {'cartItems': cart_item, 'order': order, 'items': items}


def guest_order(request, data_json):
    print('User is not authorised')
    name = data_json['form']['name']
    email = data_json['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()
    order = Order.objects.create(
        customer=customer,
        complete=False
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
