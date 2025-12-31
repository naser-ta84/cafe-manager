from django.urls import path
from .views import menu_list, add_to_cart, cart_detail,checkout

app_name = 'menu'
urlpatterns = [
    path('menu_list/', menu_list, name='menu_list'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('checkout/', checkout, name='checkout'),
]
