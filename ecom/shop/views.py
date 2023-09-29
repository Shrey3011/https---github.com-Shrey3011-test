from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth  import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import *
from .forms import *
from django.contrib import messages
from .decorators import *

# Create your views here.

@unauthenticated_user 
def register(request):

    form=CreateUserForm()

    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            username= form.cleaned_data.get('username')

            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            messages.success(request,'Account was created for ' + username)
            return redirect('login')

    context={'form':form}
    return render(request,'shop/register.html',context)

@unauthenticated_user
def login_handler(request):

    context={}
    if request.method=='POST':
        username =request.POST.get('username')
        password =request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request,'shop/login.html',context)


    return render(request,'shop/login.html',context)

def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def user_page(request):
    orders=request.user.customer.order_set.all()
    total_order=orders.count()
    orders_delivered=orders.filter(status="Delivered").count()
    orders_pending=orders.filter(status='Pending').count()
    context={'orders':orders,'customer':customer,'total_order':total_order,'orders_delivered':orders_delivered,'orders_pending':orders_pending}
    return render(request,'shop/user_page.html',context)
    
@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def account_setting(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            

    context={'form':form}
    return render(request,'shop/account_setting.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders=Order.objects.all()
    customer=Customer.objects.all()
    total_order=orders.count()
    orders_delivered=orders.filter(status="Delivered").count()
    orders_pending=orders.filter(status='Pending').count()
    context={'orders':orders,'customer':customer,'total_order':total_order,'orders_delivered':orders_delivered,'orders_pending':orders_pending}
    return render(request,'shop/dashboard.html',context)

@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'shop/products.html',context)

@login_required(login_url='login')
def customer(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()
    context={'customer':customer,'orders':orders,'count':order_count}
    return render(request,'shop/customer.html',context)

@login_required(login_url='login')
def order_form(request):

    form=Orderform()
    if request.method =='POST':
        form=Orderform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    

    context={'form':form}
    return render(request,'shop/order_form.html',context)

@login_required(login_url='login')
def update_order(request,pk):
 
    order=Order.objects.get(id=pk)
    form=Orderform(instance=order)
    if request.method =='POST':
        form=Orderform(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request,'shop/order_form.html',context)

@login_required(login_url='login')
def delete_order(request,pk):
    order=Order.objects.get(id=pk)

    if request.method=="POST":
        order.delete()
        return redirect('/') 

    context={'item':order}
    return render(request, 'shop/delete.html',context)