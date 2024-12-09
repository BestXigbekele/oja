from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='home'),

    path('cart/',views.cart,name='cart'),
    path('remove/<int:product_id>',views.remove_from_cart,name='remove'),
    path('added/<int:product_id>',views.add_to_cart,name='add_to_cart'),

    path('login',views.login_user,name='register'),
    path('logout',views.logout_user,name='logout'),
    path('Admin_site',views.admin_site,name='admin_site'),
    path('Register',views.registeruser,name='signup'),

    path('products',views.product_by_cate,name='products'),
    path('product/<str:proname>',views.product_detail,name='pro_detail'),
    path('products/<str:category>',views.product_by_cate,name='product_by_category'),

    path('checkout',views.checkout,name='checkout'),
    path('checkout_confirmation/<int:order_id>',views.confirmation,name='checkout_confirmation'),

    path('increment/<int:product_id>/',views.incremental,name='increment'),
    path('decrement/<int:product_id>/',views.decrement,name='decrement'),

]