from catalog.models import Category, Producer, Discount, Promocode, Product
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from catalog.serializers import CategorySerializer, ProducerSerializer, DiscountSerializer, \
    PromocodeSerializer, ProductSerializer


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer


class CategoryProductsView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProducersListView(ListAPIView):
    queryset = Producer.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = ProducerSerializer


class ProducerProductsView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, producer_id):
        queryset = Product.objects.filter(producer__id=producer_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountsListView(ListAPIView):
    queryset = Discount.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = DiscountSerializer


class DiscountProductsView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, discount_id):
        if discount_id == 0:
            queryset = Product.objects.filter(discount=None)
        elif discount_id > 0:
            queryset = Product.objects.filter(discount__id=discount_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class PromocodesListView(ListAPIView):
    queryset = Promocode.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = PromocodeSerializer


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = ProductSerializer
