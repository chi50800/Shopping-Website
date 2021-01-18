from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from mizi_app.models import *
import json
from django.contrib.auth.models import User
import datetime
from . utils import *
from . forms import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def store(request):
    context=carData(request)
    products=Product.objects.all()
    context['products']=products
    return render(request,'store/store.html',context)

def cart(request):
    context=carData(request)
    return render(request,'store/cart.html',context)

def contact(request):
    context=carData(request)
    return render(request,'store/contact.html',context)


#@csrf_exempt
def checkout(request):
    context=carData(request)
    return render(request,'store/checkout.html',context)

def loginPage(request):
    context=carData(request)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            customer=Customer.objects.get_or_create(user=user,name=username,email=user.email)
            return redirect('main')
        else:
            print('None')
            messages.info(request,'Wrong inputs')
    return render(request,'store/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('main')

def sign_up(request):
    context=carData(request)
    form=CreateUserForm()

    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created')
            return redirect('login')

    context['form']=form
    return render(request,'store/sign_up.html',context)

def forgot_password(request):
    context=carData(request)
    return render(request,'store/forgot_password.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('Action',action,'\nProductId',productId)
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


#@csrf_exempt
def processOrder(request):

    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
    else:
        customer,order=guestOrder(request,data)

    total=float(data['form']['total'])
    order.transaction_id=transaction_id

    if total == float(order.get_cart_total()):
        order.complete=True
    order.save()

    if order.shipping() == True:
            #print('Hey')
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )
    else:
        print('No')
    return JsonResponse('Payment Complete',safe=False)

def desc(request,id):
    context=carData(request)
    product=Product.objects.get(id=id)
    context['desc']=product
    return render(request,'store/desc.html',context)

def cust(request,id):
    context=carData(request)
    user=context['customer']
    custmer=Customer.objects.get(id=id)
    order=Order.objects.filter(customer=custmer)
    m=[]
    for ord in order:
        orderItem=ord.orderitem_set.all()
        for item in orderItem:
            m.append(item)
    context['summary']=m
    return render(request,'store/customer.html',context)