from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Product, ProductImage
from categories.models import Category
from .utils import multiple_image_upload
from .serializers import ProductSerializer, ProductImageSerializer


class ProductListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            # provide the category name not the category id when create a product
            try:
                category_name = request.data.get("category")
                category = Category.objects.get(name=category_name)
                serializer.save(category=category)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Category.DoesNotExist:
                return Response(
                    {"detail": "Category Does Not Exi."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exi."}, status=status.HTTP_404_NOT_FOUND
            )

    def put(sefl, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(
                {"detail": "Product deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
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

    """ List all images for single product based on the product id """

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
                if serializer.is_valid():
                    serializer.save(product=product)
                    uploaded_images.append(serializer.data)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            """Handel Single Images Upload"""
            serializer = ProductImageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                uploaded_images.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(uploaded_images, status=status.HTTP_201_CREATED)


class ProductImageRetrieveUpdateDestroyView(generics.RetrieveUpdateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

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

            if serializer.is_valid():
                serializer.save(product=product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ProductImage.DoesNotExist:
            return Response(
                {"detail": "Product Image Does Not Exist."},
                status=status.HTTP_404_NOT_FOUND,
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

        image.delete()
        return Response(
            {"detail": "Product Image deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductImagesDeleteSingleImageView(APIView):
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

        image.delete()
        return Response(
            {"detail": "Product Image deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductImagesDeleteAllImagesView(APIView):
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product Does Not Exist."}, status=status.HTTP_404_NOT_FOUND
            )

        ProductImage.objects.filter(product=product).delete()
        return Response(
            {"detail": "All Product Images deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
