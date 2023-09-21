from rest_framework import serializers

from .models import Order, OrderItem
from products.serializers import ProductListCreateSerializer
from products.models import Product



class ProductItemInfoSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductItemInfoSerializer()
    class Meta:
        model = OrderItem
        exclude = ('order',)

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='id')  # Rename 'id' to 'order_id'
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()



    def get_items_count(self, obj):
        return obj.items.count()

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.first_name,
            "email": obj.user.email,
        }

    def get_total_price(self, obj):
        return obj.calculate_total_price()

    
    class Meta:
        model = Order
        exclude = ('id', )





