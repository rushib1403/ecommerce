from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Product,Order,User,OrderItem,ShippingAddress,Customer,BlogComment,BookSerializer
from math import ceil
import datetime
from django.http import JsonResponse
import json
import requests
from rest_framework.decorators import api_view
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
import subprocess
import os
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from .models import *
MERCHANT_KEY = '43@KVFFXcKDRsuod'
import time
from django.utils import timezone



def tables2(request):

    user=request.user.id
    #orders =OrderItem.objects.filter(order__customer=user).order_by('-id')
    orders2=Order.objects.filter(complete=True).order_by('-id')
    print(orders2)
    return render(request,'admin/tables2.html',{'orders2':orders2})
    


def checkmail(request):
    code=request.GET['code']
    print(code)
    try:
        user=User.objects.get(email=code)
        return HttpResponse('True')
    except:
        return HttpResponse('False')




def sendcoupon(request):
    if request.method=='POST':
        discount=request.POST.get('fname2',None)
        username=request.POST.get('lname2',None)
        valid_from=request.POST.get('lname3',None)
        valid_to=request.POST.get('lname4',None)
        discount=int(discount)
        import random
        def generate(unique):
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            while True:
                value = "".join(random.choice(chars) for _ in range(6))
                if value not in unique:
                    unique.add(value)
                    break
        code = set()
        generate(code)
        code=list(code)
        user=User.objects.get(username=username)
        print(user)
        coupon=Coupon(user3=user, code=code[0], value=discount, valid_from=valid_from, valid_to=valid_to, active=True)
        print(coupon)
        coupon.save()
        notification=Notification(user=user, notification="Congradulations!!You got Coupon use code: "+ str(code) + "  to get " + str(discount) +  "%"+  "discount valid from " + str(valid_from)+  "to "+  str(valid_to), is_seen=False)
        notification.save()
    return HttpResponseRedirect('/userinfo')



def checkcoupon(request):
    code=request.GET['code']
    print(code)
    now=timezone.now()
    try:
        coupon=Coupon.objects.get(code=code,valid_from__lte=now,valid_to__gte=now,active=True,user3=request.user)
        value=coupon.value
        
        return JsonResponse(data={'value':value},safe=False)
    except:
        return HttpResponse('False')
    

    #dict1=Notification.objects.filter(user__username=request.user).order_by('-id')
    return render(request,'shop/exam.html',{})



def exam(request):
    dict1=Notification.objects.filter(user__username=request.user).order_by('-id')
    return render(request,'shop/exam.html',{'dict1':dict1})



def userinfo(request):
    orders=Order.objects.all()
    dict1={}
    
    for j in orders:
        dict1[j.customer.user.username]=0
    for i in orders:
        dict1[i.customer.user.username]+=1
    print(dict1)
    params={'dict1':dict1}
    
    #return render(request,'shop/userinfo.html',params)
    return render(request,'admin/tables.html',params)


def adminpanel(request):
    dict1=Notification.objects.filter(user__username=request.user).order_by('-id')[:5]
    user_count=User.objects.all().count()
    order=Order.objects.all()
    return render(request,'admin/index.html',{'dict1':dict1,'user_count':user_count})

def categorywise_all(request):
    allProds = []
    catprods = Product.objects.values('categories', 'id')
    cats = {item['categories'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(categories=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    print(params)
    return render(request,'shop/index.html',params)

def chatjava(request):
    #user=request.user.username 
    user=request.session['loginuser']
    #=user
    #response=HttpResponse(user)
    #response.set_cookie('java_tut')
    #return response
    data={'user':user}
    return JsonResponse(data,safe=False)

def track(request):
    user=request.user.id
    id=request.GET['id']
    order=Order.objects.get(id=id)
    if order.status2 == 'Order Recieved':
        progress_percentage = 20
    elif order.status2 == 'preparing':
        progress_percentage = 40
    elif order.status2 == 'prepared':
        progress_percentage = 60
    elif order.status2 == 'Out for delivery':
        progress_percentage = 80
    elif order.status2 == 'delivered':
        progress_percentage = 100
    
    """ orders =OrderItem.objects.filter(order__customer=user)
    orders2=OrderItem.objects.all()
    value=request.GET['value']
    id=request.GET['id']
    order=OrderItem.objects.filter(order=id)
    print(order) """
    return render(request,'tracker.html',{'order':order,'progress':progress_percentage})
def sendstatus(request):
    user=request.user.id
    orders =OrderItem.objects.filter(order__customer=user)
    orders2=Order.objects.all().order_by('-id')
    value=request.GET['value']
    id=request.GET['id']
    order=Order.objects.get(id=id)
    print(order)
    order.status2=value
    order.save()
    return render(request,'admin/tables2.html',{'orders':orders,'orders2':orders2})

def prevorder(request):

    user=request.user.id
    orders =OrderItem.objects.filter(order__customer=user).order_by('-id')
    orders2=Order.objects.filter(complete=True).order_by('-id')
    print(orders2)
    return render(request,'orders.html',{'orders':orders,'orders2':orders2})

# Create your views here.
def search(request):
    list=[]
    inf=request.GET['i']
    product=Product.objects.filter(categories__icontains=inf)
    product2=Product.objects.filter(name__icontains=inf)
    product3=product.union(product2)
    print(type(product3))
    context={'product3':product3}
    #question2=Question.objects.filter(question_no=id,exam_name__exam_name=examname)

    for i in product3:
        serializer= BookSerializer(i)
        list.append(serializer.data)
    import json
    return HttpResponse(json.dumps(list))
    #return JsonResponse(product3,safe=False)
    #return render(request,'main.html',context)


def blogpost(request, slug):
    post=Product.objects.filter(slug=slug).first()
    comment=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post,'comment':comment,'user':request.user,'replyDict':replyDict}
    return render(request,'blog/blogpost.html',context)

def postComment(request):
    if request.method=='POST':
        comment=request.POST.get("comment")
        user=request.user
        postsno=request.POST.get("postsno")
        post=Product.objects.get(id=postsno)
        parentsno=request.POST.get("parentsno")
        if parentsno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,'comment posted succesfully')
        else:
            parent=BlogComment.objects.get(sno=parentsno)

            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,'Reply posted succesfully')


    return HttpResponseRedirect(f'/')
def store(request):

    try:
        m=request.GET['value']
        print(m)
        product=Product.objects.filter(categories=m)
        print(product)
    except:
        product=Product.objects.all()
    #else:
    #    product=Product.objects.all()

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartitems=order['get_cart_items']
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        if cart is not None:
            for i in cart:
                try:
                    cartitems+=cart[i]
                    product2=Product.objects.get(id=i)
                    total=(product2.price * cart[i])
                    items.append([product2,total,cart[i]])
                    order['get_cart_total']+=total
                    order['get_cart_items']+=cart[i]
                except:
                    pass
    print('hii')

    context={'items':items,'product':product,'cartitems':cartitems}
    print(product)
    return render(request,'shop/store.html',context)
    #return render(request,'admin/index.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        print(order)
        items=order.orderitem_set.all()
        cartitems=order.get_cart_items

    else:
        order={'get_cart_total':0,'get_cart_items':0}
        cartitems=order['get_cart_items']
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        if cart is not None:
            for i in cart:
                try:
                    cartitems+=cart[i]
                    product=Product.objects.get(id=i)
                    total=(product.price * cart[i])
                    items.append([product,total,cart[i]])
                    order['get_cart_total']+=total
                    order['get_cart_items']+=cart[i]
                except:
                    pass
    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'shop/cart.html',context)



def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        #order=Order.objects.filter(customer=customer,complete=False).first()
        print(order)
        items=order.orderitem_set.all()
        #total=sum([item.product.price*item.quantity for item in items])
        #total=[item.product.price*item.quantity for item in items]
        cartitems=order.get_cart_items
        #print(total)
        #total=items.product.price*items.quantity
        #rint(items)
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0}
        cartitems=order['get_cart_items']
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        items=[]
        if cart is not None:
            for i in cart:
                try:
                    cartitems+=cart[i]
                    product=Product.objects.get(id=i)
                    total=(product.price * cart[i])
                    items.append([product,total,cart[i]])
                    order['get_cart_total']+=total
                    order['get_cart_items']+=cart[i]
                except:
                    pass
    context={'items':items,'order':order,'cartitems':cartitems}
    return render(request,'shop/checkout.html',context)
def updateitem(request):
    productid=request.GET.get('productid',None)
    action=request.GET['action']
    print(action)
    customer=request.user.customer
    product=Product.objects.get(id=productid)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderitem.quantity+=1
    if action=='remove':
        orderitem.quantity=(orderitem.quantity - 1)
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    return JsonResponse('item were added',safe=False)
def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    name=request.GET.get('name','AnonymousUser')
    email=request.GET.get('email','AnonymousUser')
    address=request.GET.get('address','AnonymousUser')
    zipcode=request.GET.get('zipcode','AnonymousUser')
    country=request.GET.get('country','AnonymousUser')
    city=request.GET.get('city','AnonymousUser')
    state=request.GET.get('state','AnonymousUser')
    discount=request.GET.get('discount',None)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total =order.get_cart_total
    if discount==None:
        print("none")
    else:
        now=timezone.now()
        try:
            coupon=Coupon.objects.get(code=discount,valid_from__lte=now,valid_to__gte=now,active=True,user3=request.user)
            discount_value=coupon.value
            total=total-(total*discount_value)/100
            print(total)
            coupon.active=False
            coupon.save()
        except:
            pass
    order.complete = True
    order.discounted_price=total
    order.transaction_id = transaction_id
    order.save()
    ShippingAddress.objects.create(customer=customer,order=order,address=address,city=city,state=state,zipcode=zipcode)
    #return HttpResponse('Transaction Completed')
    param_dict = {

                'MID': 'WMigrU07941955034284',
                'ORDER_ID': str(transaction_id),
                'TXN_AMOUNT': str(total),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8081/handlerequest/',

        }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    return render(request, 'shop/paytm.html', {'param_dict': param_dict})




@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})






def processorder2(request):
    transaction_id = datetime.datetime.now().timestamp()
    name=request.GET.get('name',None)
    email=request.GET.get('email',None)
    address=request.GET.get('address',None)
    zipcode=request.GET.get('zipcode',None)
    country=request.GET.get('country',None)
    city=request.GET.get('city',None)
    state=request.GET.get('state',None)
    customer=name
    order, created = Order.objects.get_or_create(customer__name=customer, complete=False)
    print(order.complete)

    order2={'get_cart_total':0,'get_cart_items':0}
    cartitems=order2['get_cart_items']
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    items=[]
    for i in cart:
        try:
            cartitems+=cart[i]
            product=Product.objects.get(id=i)
            total=(product.price * cart[i])
            items.append([product,total,cart[i]])
            order2['get_cart_total']+=total
            order2['get_cart_items']+=cart[i]
        except:
            pass
    total =order2['get_cart_total']



    order.complete = True
    #delete_cookie('cart')
    order.transaction_id = transaction_id
    order.save()
    #order.complete = True

    #order.save()
    customer=Customer.objects.create(name=name,email=email)
    ShippingAddress.objects.create(customer=customer,order=order,address=address,city=city,state=state,zipcode=zipcode)
    return HttpResponse('Transaction Completed')
from jpype import *
from shop import pkg

def contact2(request):
    name=request.GET['name']
    email=request.GET['email']
    user=User.objects.get(username="pankajpalmate")

    message=request.GET['message']
    notification=Notification(user=user,notification=message + "From  " + email ,is_seen=False)
    notification.save()

    return render(request,'shop/store.html')

def contact(request):

    return render(request,'shop/contact.html')

    #return render(request,'shop/contact.html')
def handlesignup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters!")
            return HttpResponseRedirect('/')

        if password1!=password2:
            messages.error(request,"Paasword not matched!")
            return HttpResponseRedirect('/')

        #creating user
        myuser=User.objects.create_user(username,email,password1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"your account has been succesfully created!")
        return HttpResponseRedirect('/')


    else:
        return HttpResponse('Error 404-not found')
def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['username2']
        request.session['loginuser']=loginusername
        password=request.POST['password']
        user=authenticate(username=loginusername,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'successfully logged in')
            return HttpResponseRedirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            return HttpResponseRedirect('/')

    return HttpResponse('Error 404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request,'Succesfully Logged out')
    return HttpResponseRedirect('/')
def category(request):
    return render(request,'index.html')

def viewprod(request):
    n=request.GET['value2']
    post=Product.objects.filter(id=n).first()
    comment=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    l=int(n)
    print(type(l))
    product=Product.objects.get(id=l)
    if request.user.is_authenticated:
            customer=request.user.customer
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            items=order.orderitem_set.all()
            cartitems=order.get_cart_items
    else:
            items=[]
            order={'get_cart_total':0,'get_cart_items':0}
            cartitems=order['get_cart_items']
            try:
                cart=json.loads(request.COOKIES['cart'])
            except:
                cart={}
            items=[]
            if cart is not None:
                for i in cart:
                    try:
                        cartitems+=cart[i]
                        product=Product2.objects.get(id=i)
                        total=(product2.price * cart[i])
                        items.append([product2,total,cart[i]])
                        order['get_cart_total']+=total
                        order['get_cart_items']+=cart[i]
                    except:
                        pass
    context={'post':post,'comment':comment,'user':request.user,'replyDict':replyDict,'product':product,'items':items,'cartitems':cartitems}
    return render(request,'shop/viewprod.html',context)
