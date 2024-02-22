from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('about/', views.about, name="about"),
    path('index/', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('product/', views.product, name="product"),
    path('shop/', views.shop, name="shop"),

]