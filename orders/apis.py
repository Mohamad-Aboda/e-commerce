from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, OrderItemCreateUpdateSerializer
from .permissions import ProductListCreateCustomPermission, ProductRetrieveDestroyPermission, ProductItemPermission

User = get_user_model()

class OrderListCreateView(APIView):
    permission_classes = [ProductListCreateCustomPermission]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: OrderSerializer(many=True)},
            manual_parameters=[
                openapi.Parameter(
                    name="Authorization",
                    in_=openapi.IN_HEADER,
                    type=openapi.TYPE_STRING,
                    description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def get(self, request):
        """ List all user orders """
        user = request.user
        if user.is_authenticated:  # Check if the user is authenticated
            orders = Order.objects.filter(user=user)
            if orders:
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "You don't have any orders yet."},
                                status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={status.HTTP_201_CREATED: OrderSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        order = Order.objects.create(user=user)
        serializer = OrderSerializer(order)
        return Response({"msg":"Order created successfully", "order_details":serializer.data},
                         status=status.HTTP_201_CREATED)


class OrderRetrieveDestroyView(APIView):
    permission_classes = [ProductRetrieveDestroyPermission]

    def get_order(self, order_pk):
        try:
            order = Order.objects.get(pk=order_pk)
            if order.user == self.request.user:return order
            else:return None # not the order owner
        except Order.DoesNotExist: # order does not exist in the database
            return None

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: OrderSerializer()},
            manual_parameters=[
                openapi.Parameter(
                    name="Authorization",
                    in_=openapi.IN_HEADER,
                    type=openapi.TYPE_STRING,
                    description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def get(self, request, order_pk):
        order = self.get_order(order_pk)
        if order:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": "Order not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Order deleted successfully."},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def delete(self, request, order_pk):
        user = request.user
        if user.is_authenticated:
            order = self.get_order(order_pk)
            if order:
                order.delete()
                return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "Order not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)


class OrderItemListCreateView(APIView):
    permission_classes = [ProductItemPermission]

    def get_order(self, order_pk):
        try:
            order = Order.objects.get(pk=order_pk)
            # Check if the order belongs to the authenticated user
            if order.user == self.request.user:
                return order
            else:
                return None
        except Order.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: OrderItemSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def get(self, request, order_pk):
        order = self.get_order(order_pk)
        if order:
            items = OrderItem.objects.filter(order=order)
            if items.count() > 0:
                serializer = OrderItemSerializer(items, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Order does not contains items yet."}, status=status.HTTP_200_OK)

        return Response({"detail": "Order not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=OrderItemCreateUpdateSerializer,
        responses={status.HTTP_201_CREATED: OrderItemCreateUpdateSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def post(self, request, order_pk):
        """ Add items to existing order """
        order = self.get_order(order_pk)
        if order:
            serializer = OrderItemCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                # Check if the product belongs to the authenticated user
                product = serializer.validated_data['product']
                if product.user == request.user:
                    serializer.save(order=order)
                    return Response({"msg":"items added to order succefully", "details":serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "You don't have permission to add this item."}, status=status.HTTP_403_FORBIDDEN)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Order not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)



class OrderItemRetrieveUpdateDestroyView(APIView):
    permission_classes = [ProductItemPermission]

    def get_order_item(self, order_pk, item_pk):
        try:
            order_item = OrderItem.objects.get(order__pk=order_pk, pk=item_pk)
            # Check if the order item belongs to the authenticated user
            if order_item.order.user == self.request.user:
                return order_item
            else:
                return None
        except OrderItem.DoesNotExist:
            return None


    @swagger_auto_schema(
        responses={status.HTTP_200_OK: OrderItemSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def get(self, request, order_pk, item_pk):
        order_item = self.get_order_item(order_pk, item_pk)
        if order_item:
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Order item not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=OrderItemCreateUpdateSerializer,
        responses={status.HTTP_200_OK: OrderItemCreateUpdateSerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def put(self, request, order_pk, item_pk):
        order_item = self.get_order_item(order_pk, item_pk)
        if order_item:
            serializer = OrderItemCreateUpdateSerializer(order_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Order item not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Order item deleted successfully."},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def delete(self, request, order_pk, item_pk):
        order_item = self.get_order_item(order_pk, item_pk)
        if order_item:
            order_item.delete()
            return Response({"detail": "Order item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Order item not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
