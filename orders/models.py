from django.db import models
from django.contrib.auth import get_user_model

from categories.models import Category

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Oder Number ({self.pk})"
    
    def calculate_total_price(self):
        total_price = 0
        for item in self.items.all():
            total_price += item.product.price * item.quantity
        return total_price



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items' , on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order Number ( {self.pk} ) For {self.order}"


