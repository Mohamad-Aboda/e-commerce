from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly
from .models import Category
from .utils import get_category


class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CategorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_201_CREATED: CategorySerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            category_name = request.data.get('name')
            if Category.objects.filter(name=category_name).exists():
                return Response({"detail": "Category with this name already exists."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

class CategoryRetriveUpdateDestroyView(APIView):
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:  # Apply IsAdminOrReadOnly permission for PUT, PATCH, DELETE methods
            permission_classes = [IsAdminOrReadOnly]
        else:  # For other methods, use default permissions (AllowAny)
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CategorySerializer()}
    )
    def get(self, request, pk):
        category = get_category(pk)
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_200_OK: CategorySerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def put(self, request, pk):
        category = get_category(pk)
        if category:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
    

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={status.HTTP_200_OK: CategorySerializer()},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def patch(self, request, pk):
        category = get_category(pk)
        if category:
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Category deleted successfully."},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def delete(self, request, pk):
        category = get_category(pk)
        if category:
            category.delete()
            return Response({"detail": "Category deleted successfully."},status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
