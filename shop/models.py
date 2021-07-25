from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User,auth
from rest_framework import serializers
import json
from django.db.models.signals import *
from django.dispatch import receiver
# Create your models here.
from django.utils.timezone import now
from channels.layers import  get_channel_layer
from asgiref.sync import async_to_sync
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Coupon(models.Model):
    user3=models.ForeignKey(User, on_delete=models.CASCADE)        
    code=models.CharField(max_length=50,unique=True)
    value=models.IntegerField(default=0)
    valid_from=models.DateTimeField()
    valid_to=models.DateTimeField()
    active=models.BooleanField()
   
class Notification(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    notification=models.TextField(max_length=100)
    is_seen=models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        print("save called")
        channel_layer=get_channel_layer()
        notification_objs=Notification.objects.filter(is_seen=False).count()
        data={'count':notification_objs,'current_notification':self.notification}
        user2=self.user.username
        async_to_sync(channel_layer.group_send)(
            'order_' + user2 ,{

                'type':'send_notification2',
                'value':json.dumps(data)
            }
        )
        super(Notification,self).save(*args,**kwargs)




class Product(models.Model):
    category = [
    ('allcat', 'allcat'),
    ('mobiles', 'mobiles'),
    ('tvs', 'tvs'),
    ('headphones', 'headphones'),
    ('homeappliences', 'homeappliences'),
    ('laptops','laptops'),
    ('menwear','menwear'),
    ('ornaments','ornaments'),
    ('footwear','footwear'),
    ('shirts','shirts'),
    ('womenwear','womenwear'),
    ('pantsmen','pantsmen'),
    ]
    subcategory=[
    ('men','men'),
    ('women','women'),
        
    ]
    subcategory=models.CharField(max_length=40,choices=subcategory,null=True,blank=True)
    categories = models.CharField(max_length=40,choices=category,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=False)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class BookSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    categories=serializers.CharField(max_length=40)
    name=serializers.CharField(max_length=200)
    price=serializers.FloatField()
    image=serializers.ImageField()

CHOICES = (
    ("Order Recieved", "Order Recieved"),
    ("preparing", "preparing"),
    ("prepared", "prepared"),
    ("Out for delivery", "Out for delivery"),
    ("delivered", "delivered"),
    
    
    
    
)
 

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)
    status2 = models.CharField(max_length=100 , choices = CHOICES , default="Order Recieved")
    discounted_price=models.FloatField(blank=True,null=True)
    #order=orderitem_set.all()
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        #print(self.transaction_id)
        orderitems =self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @staticmethod
    def get_total_orders(self):
        return Order.objects.filter(customer=self.customer).count()
        



class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)
    @property
    def get_total(self):
        total=self.product.price *self.quantity
        return total
""" 
@receiver(post_save,sender=OrderItem)
def order_status_handler(sender,instance,created,**kwargs):
    if not created:
        channel_layer=get_channel_layer()
        data={}
        data['progress']=instance.status
        async_to_sync(channel_layer.group_send)(
            'order_'+f'{instance.id}',{

                'type':'order_status',
                'value':json.dumps(data['progress'])
            }
        ) """
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance,created , **kwargs):

    if not created:
        print("###################")
        channel_layer = get_channel_layer()
        data  = {}
        data['order_id'] = instance.id
        #data['amount'] = instance.amount
        data['status2'] = instance.status2
        #data['date'] = str(instance.date)
        progress_percentage = 20
        if instance.status2 == 'Order Recieved':
            progress_percentage = 20
        elif instance.status2 == 'preparing':
            progress_percentage = 40
        elif instance.status2 == 'prepared':
            progress_percentage = 60
        elif instance.status2 == 'Out for delivery':
            progress_percentage = 80
        elif instance.status2 == 'delivered':
            progress_percentage = 100
    
        
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.id,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    phone=models.CharField(max_length=13)
    email=models.CharField(max_length=50)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.name
class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    photo=models.ImageField(default="media/gallery/admin.png")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Product,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:13] +"..."+"by" + self.user.username
