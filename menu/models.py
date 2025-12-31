from django.db import models
from django.conf import settings
from booking.models import Table

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته بندی")

    def __str__(self):
        return self.name
class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='items')
    name = models.CharField(max_length=100,verbose_name="نام ایتم")
    description = models.TextField(verbose_name="توضیحات")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    image = models.ImageField(upload_to='menu_items/',verbose_name="تصویر")
    is_available = models.BooleanField(default=True,verbose_name="موجود است؟")

    def __str__(self):
        return self.name
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"سفارش {self.id} - میز {self.table.number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} عدد {self.product.name}"