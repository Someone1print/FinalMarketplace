from django.http import Http404
from rest_framework import permissions, status, filters
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer, CartSerializer
from .models import Product, Cart
from users.permissions import IsVendorPermission, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser


class ProductCreateAPIView(APIView):
    permission_classes = [IsVendorPermission]

    # authentication_classes = []
    # parser_classes = JSONParser

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                name=request.data['name'],
                vendor_id=request.data['vendor'],
                category_id=request.data['category'],
                description=request.data['description'],
                price=request.data['price']
            )
            product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'name', 'description']
    search_fields = ['price', 'name', 'description']
    # это метод viewset к которому нельзя присоеденить поиск
    # def get(self, request):
    #     snippets = Product.objects.all()
    #     serializer = ProductSerializer(snippets, many=True)
    #     return Response(serializer.data)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        qs = Product.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs


class ProductDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        snippet = self.get_object(id)
        serializer = ProductSerializer(snippet)
        return Response(serializer.data)


def get_object(id):
    try:
        return Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404


class ProductUpdateAPIView(APIView):
    permission_classes = [IsVendorPermission, IsOwnerOrReadOnly]
    # authentication_classes = []

    def put(self, request, id):
        snippet = get_object(id)
        serializer = ProductSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsVendorPermission, IsOwnerOrReadOnly]
    # authentication_classes = []

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, id):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class AddToCartAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    # parser_classes = JSONParser

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Cart.DoesNotExist:
            raise Http404

    def put(self, request, user_id):
        snippet = self.get_object(user_id)
        serializer = CartSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    # parser_classes = JSONParser

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        cart = self.get_object(user_id)
        serializer1 = CartSerializer(cart)
        serializer2 = ProductSerializer(cart.product.all(), many=True)
        data = serializer1.data
        data['product'] = serializer2.data
        return Response(data, status=status.HTTP_200_OK)
