from rest_framework import serializers

from .models import Product, ProductImage


class ProductListCreateSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "user"]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.first_name,
            "email": obj.user.email,
        }
    def validate_name(self, value):
        user = self.context['request'].user
        if Product.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError('You already have a product with this name.')
        return value


class ProductRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "user"]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.first_name,
            "email": obj.user.email,
        }


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
