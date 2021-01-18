import json
from . models import *

def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
            cart={}
    print(cart)
    items=[]
    order={'get_item_count':0,'get_cart_total':0,'shipping':False}
    cartItems=order['get_item_count']

    for i in cart:
        try:
            cartItems+=cart[i]['quantity']

            product=Product.objects.get(id=i)
            total=(product.price * cart[i]['quantity'])

            order['get_cart_total']+=total
            order['get_item_count']+=cart[i]['quantity']

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'geturl':product.geturl
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)

            if product.digital==False:
                order['shipping']=True
        except:
            pass
    return {'items':items, 'order':order,'cartItems':cartItems}

def carData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_item_count
        context={'customer':customer,'items':items, 'order':order,'cartItems':cartItems}
    else:
        context=cookieCart(request)
        context['customer']='null'
    return context

def guestOrder(request,data):
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    context=cookieCart(request)
    items=context['items']
    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()

    order=Order.objects.create(customer=customer,complete=False)

    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem=OrderItem.objects.create(product=product,order=order,quantity=item['quantity'])

    return customer,order