from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('tables/', views.table_list, name='table_list'),
    path('reserve/<int:table_id>/', views.reserve_table, name='reserve_table'),
]