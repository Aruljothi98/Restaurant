from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Restaurant.form import CustomUserForm
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views import generic

# Create your views here.
class about(generic.ListView):
    model= menu
    template_name="shop/about.html"


def home(request):
    List=list.objects.filter(trending=1)
    return render(request,"shop/index.html",{"List":List})

def register(request):
    return render(request,"shop/register.html")

def menu_page(request):
    Menu=menu.objects.filter(status=0)
    return render(request,"shop/menu.html",{"Menu":Menu})


def menus_view(request,name):
    if(menu.objects.filter(name=name,status=0)):
        List=list.objects.filter(Menu__name=name)
        return render(request,"shop/lists/index.html",{"List":List,"menu_name":name})
    else:
        messages.warning(request, "NO such catagory found")
        return redirect("menu")
    
def list_details(request,cname,pname):
    if(menu.objects.filter(name=cname,status=0)):
        if(list.objects.filter(name=pname,status=0)):
            List=list.objects.filter(name=pname,status=0).first()
            return render(request,"shop/lists/list_details.html",{"List":List})
        else:
            messages.warning(request, "NO such menus are found")
            return redirect("menu")
    else:
        messages.warning(request, "NO such menus are  found")
        return redirect("menu")
    
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registeration success you can log now ")
            return redirect('/login')
    return render(request,"shop/register.html",{"form":form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            User=authenticate(request,username=name,password=pwd)
            if User is not None:
                login(request,User)
                messages.success(request,"login successfully")
                return redirect('/')
            else:
                messages.error(request,"invalid username or password")
                return redirect('/login')
    return render(request,"shop/login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logged out successfully")
    return redirect('/')

def remove_to_fav(request,cid):
    cartitem=Favourite.objects.get(id=cid)
    cartitem.delete()
    return redirect('/fav')

def fav_page(request):
    if request.user.is_authenticated:
        favourite=Favourite.objects.filter(User=request.user)
        return render(request,"shop/fav.html",{"favourite":favourite})
    else:
        return redirect('/')
    

def favourite_page(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            list_id=data['pid']
            #print(request.user.id)
            list_status=list.objects.get(id=list_id)
            if list_status:
                if Favourite.objects.filter(User=request.user.id,list_id=list_id):
                    return JsonResponse({'status':'Item Already in Favourite'},status=200)
                else:
                    Favourite.objects.create(User=request.user,list_id=list_id)
                    return JsonResponse({'status':'Favourite Item is Available'},status=200)
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    



def remove_to_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(User=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect('/')

def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            list_qty=data['list_qty']
            list_id=data['pid']
            #print(request.user.id)
            list_status=list.objects.get(id=list_id)
            if list_status:
                if Cart.objects.filter(User=request.user.id,list_id=list_id):
                    return JsonResponse({'status':'Item Already in cart'},status=200)
                else:
                    if list_status.quantity>=list_qty:
                        Cart.objects.create(User=request.user,list_id=list_id,list_qty=list_qty)
                        return JsonResponse({'status':'Item Added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Item Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to add cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        body=request.POST.get('body')
        print(name,email,body)
        send_mail(
            'caddcenter - chat',
            name + "-" +body,
            email,
            ['ratha98arul@gmail.com'],
            fail_silently=False,
        )
        
    return render(request,"shop/contacts.html")

def order_page(request):
    return render(request,"shop/order.html")
   





