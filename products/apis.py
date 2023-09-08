from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Product, ProductImage
from categories.models import Category
from .utils import multiple_image_upload
from .serializers import (
    ProductListCreateSerializer,
    ProductImageSerializer,
    ProductRetrieveUpdateDestroySerializer,
)
from .permissions import IsOwnerOrReadOnly


class ProductListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductListCreateSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductListCreateSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product name"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product description"
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Product price"
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product category"
                ),
            },
        ),
        responses={
            201: "Created",
            400: "Bad Request",
        },
        operation_summary="Create a new product",
        operation_description="Create a new product with the given details.",
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
        serializer = ProductListCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # provide the category name not the category id when create a product
            try:
                category_name = request.data.get("category")
                category = Category.objects.get(name=category_name)
                product = serializer.save(category=category, user=request.user)
                response_data = serializer.data
                response_data["user"] = {
                    "id": product.user.id,
                    "username": product.user.first_name,
                    "email": product.user.email,
                }

                return Response(response_data, status=status.HTTP_201_CREATED)

            except Category.DoesNotExist:
                return Response(
                    {"detail": "Category Does Not Exi."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:  # Apply IsAdminOrReadOnly permission for PUT, PATCH, DELETE methods
            permission_classes = [IsAuthenticated]
        else:  # For other methods, use default permissions (AllowAny)
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_summary="Retrieve a product",
        operation_description="Retrieve product details by its ID.",
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductRetrieveUpdateDestroySerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exi."}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product name"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product description"
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Product price"
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product category"
                ),
            },
        ),
        responses={
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_summary="Full Update a product",
        operation_description="Full Update an existing product with the given details.",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],)
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductRetrieveUpdateDestroySerializer(
                product,
                data=request.data,
            )
            if serializer.is_valid() and request.user == product.user:
                # Check if 'category' is present in the request data
                if 'category' in request.data:
                    # Update the category by fetching the category object
                    category_name = request.data['category']
                    try:
                        category = Category.objects.get(name=category_name)
                        product.category = category
                    except Category.DoesNotExist:
                        return Response(
                            {"detail": "Category Does Not Exist."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "You do not have permission to update this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product name"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product description"
                ),
                "price": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Product price"
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Product category"
                ),
            },
        ),
        responses={
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_summary="Partial Update a product",
        operation_description="Partial Update an existing product with the given details.",
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
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductRetrieveUpdateDestroySerializer(
                product,
                data=request.data,
                partial=True
            )
            if serializer.is_valid() and request.user == product.user:
                # Check if 'category' is present in the request data
                if 'category' in request.data:
                    # Update the category by fetching the category object
                    category_name = request.data['category']
                    try:
                        category = Category.objects.get(name=category_name)
                        product.category = category
                    except Category.DoesNotExist:
                        return Response(
                            {"detail": "Category Does Not Exist."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "You do not have permission to update this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Product deleted successfully."},
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
        try:
            product = Product.objects.get(pk=pk)
            if request.user == product.user:
                product.delete()
                return Response(
                    {"detail": "Product deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {"detail": "You do not have  permission to delete this product."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exi."}, status=status.HTTP_404_NOT_FOUND
            )


class ProductImageListCreateView(APIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    """ List all images for single product based on the product id """

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductImageSerializer(many=True)},
        operation_summary="List images for a single product",
        operation_description="Retrieve a list of all images for a single product based on the product ID.",
    )
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            images = ProductImage.objects.filter(product=product)
            serializer = ProductImageSerializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

    """ Handel Single and Multipe image upload """

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        uploaded_images = []

        """ Handel Multipe Images Upload """
        if multiple_image_upload(request):
            for image_file in request.FILES.getlist("image"):
                image_data = {"image": image_file, "product": product.id}
                serializer = ProductImageSerializer(data=image_data)
                if request.user == product.user:
                    if serializer.is_valid():
                        serializer.save(product=product)
                        uploaded_images.append(serializer.data)
                    else:
                        return Response(
                            serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                    {"detail": "Yon don't have permissions to upload image for this product."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            """Handel Single Images Upload"""
            serializer = ProductImageSerializer(data=request.data)
            if request.user == product.user:
                if serializer.is_valid():
                    serializer.save(product=product)
                    uploaded_images.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                {"detail": "Yon don't have permissions to upload image for this product."}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(uploaded_images, status=status.HTTP_201_CREATED)


class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']: 
            permission_classes = [IsAuthenticated]
        else:  # For other methods, use default permissions (AllowAny)
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


    @swagger_auto_schema(
        responses={
            200: "OK",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_summary="Retrieve a product image",
        operation_description="Retrieve a product image by its ID.",
    )
    def get(self, request, product_id, image_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            image = ProductImage.objects.get(pk=image_id, product=product)
            serializer = ProductImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Product Image Does Not Exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def update(self, request, product_id, image_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            image = ProductImage.objects.get(pk=image_id, product=product)
            serializer = ProductImageSerializer(image, data=request.data)

            if serializer.is_valid() and product.user == request.user:
                serializer.save(product=product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Product Image Does Not Exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "Product Image deleted successfully."},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def delete(self, request, product_id, image_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            image = ProductImage.objects.get(pk=image_id, product=product)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Product Image Does Not Exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if product.user == request.user:
            image.delete()
            return Response(
                {"detail": "Product Image deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:    
            return Response(
                {"detail": "You do not have  permission to delete this image."},
                status=status.HTTP_403_FORBIDDEN,
            )


class ProductImagesDeleteAllImagesView(APIView):
    # permission_classes = [IsOwnerOrReadOnly]
    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: "All Product Images deleted successfully."},
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token: 'Bearer {token}'",
            ),
        ],
    )
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        if request.user == product.user:
            ProductImage.objects.filter(product=product).delete()
            return Response(
                {"detail": "All Product Images deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "You do not have  permission to delete this image."},
                status=status.HTTP_403_FORBIDDEN,
            )


# still not implemented the tests for create and udpate product images
# still not implemented swagger for create and update product images

