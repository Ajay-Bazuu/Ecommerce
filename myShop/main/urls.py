from django.urls import path
from .views import *
from main import views
urlpatterns = [
    path("",index,name="index"),
    # path("cart/",cart,name="cart"),
    path("checkout/",checkout,name="checkout"),
    path("contact/",contact,name="contact"),
    path("shop",shop,name="shop"),
    path("product_detail/<int:id>",product_detail,name="product_detail"),
    path("blog/",blog,name="blog"),
    path("blog-single/",blog_single,name="blog_single"),
    path("login/",log_in,name="log_in"),
    path("logout/",log_out,name="log_out"),
    path("register/",register,name="register"),
    path('profile/',customer_detail,name='profile'),
    path('your_order/',your_order,name='your_order'),

    # Cart Section
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    # Payments
    path('initkhalti/<int:id>',initkhalti,name='initkhalti'),
    path('verify/',verifyKhalti,name='verify'),
]
