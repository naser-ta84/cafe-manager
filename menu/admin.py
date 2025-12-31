from django.contrib import admin
from .models import Category , MenuItem , Order ,OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','is_available')
    list_filter = ('category','is_available')
    search_fields = ('name',)

class OrderItemInline(admin.TabularInline): # برای نمایش آیتم‌ها در دل سفارش
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    inlines = [OrderItemInline]