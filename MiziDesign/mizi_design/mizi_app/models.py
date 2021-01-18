from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=264,default="")
    email=models.EmailField(max_length = 264,default="")

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=264,default="Product")
    price=models.DecimalField(max_digits=7,decimal_places=2)
    digital=models.BooleanField(default=False,blank=False)
    image=models.ImageField(null=True,blank=True)
    description=models.CharField(max_length=264,null=True)

    def __str__(self):
        return self.name

    def geturl(self):
        try:
            url=self.image.url
        except:
            url=""
        return url

    def get_price(self):
        return self.price

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,blank=False)
    transaction_id=models.CharField(max_length=264,null=True)

    def __str__(self):
        return str(self.transaction_id)

    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
                break
        return shipping

    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=0
        for item in orderitems:
            total+=item.get_total()
        return total

    def get_item_count(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return self.quantity * self.product.get_price()

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True)
    address=models.CharField(max_length=264,null=True)
    city=models.CharField(max_length=264,null=True)
    state=models.CharField(max_length=264,null=True)
    zip_code=models.CharField(max_length=264,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

