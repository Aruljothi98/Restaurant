from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('menu',views.menu_page,name='menu'),
    path('menu/<str:name>',views.menus_view,name='menu'),
    path('menu/<str:cname>/<str:pname>',views.list_details,name="list_details"),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('cart',views.cart_page,name='cart'),
    path('removetocart/<str:cid>',views.remove_to_cart,name='removetocart'),
    path('favourite',views.favourite_page,name='favourite'),
    path('fav',views.fav_page,name='fav'),
    path('removetofav/<str:cid>',views.remove_to_fav,name='removetofav'),
    path('contacts',views.contact,name="contacts"),
    path('about',views.about.as_view(),name="about"),
    path('order',views.order_page,name="order"),



]