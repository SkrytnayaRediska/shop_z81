from catalog.models import Category, Producer, Discount, Promocode, Product, Basket
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from catalog.serializers import CategorySerializer, ProducerSerializer, DiscountSerializer, \
    PromocodeSerializer, ProductSerializer, BasketSerializer, AddProductSerializer, \
    DeleteProductSerializer, OrderSerializer
from django.db.models import F
from django.shortcuts import get_object_or_404
from catalog.tasks import some_task
from drf_yasg.utils import swagger_auto_schema


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = CategorySerializer



class CategoryProductsView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        some_task.delay()
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


class BasketView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_method='GET',
        responses={
            200: BasketSerializer
        },
        tags=['catalog']
    )
    def get(self, request):
        user = request.user
        basket = Product.objects.prefetch_related("basket_set").filter(basket__user=user).values(
            "name", "price", "discount", "discount__name", number_of_items=F("basket__count"),
            discount_percent=F("discount__percent"), discount_date_end=F("discount__date_end")
        )
        serializer = BasketSerializer({'products': basket})

        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=AddProductSerializer,
        request_method='POST',
        responses={
            200: ''
        },
        tags=['catalog']
    )
    def post(self, request):
        """
        number_of_items > 0 if need sum with current count of the product in cart
        number_of_items < 0 if need subtract from current count of the product in cart
        If you subtract more than user has in the basket,
            there will be no such product in the cart anymore
        """
        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data.get('product_id'))

        basket_object, _ = Basket.objects.get_or_create(user=request.user, product=product)

        if basket_object.count:
            basket_object.count += input_serializer.data.get('number_of_items')
        else:
            basket_object.count = input_serializer.data.get('number_of_items')

        if basket_object.count <= 0:
            basket_object.delete()
        else:
            basket_object.save()

        return Response()


    @swagger_auto_schema(
        request_body=DeleteProductSerializer,
        request_method='DELETE',
        responses={
            200: ''
        },
        tags=['catalog']
    )
    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data['product_id'])
        # product = Product.objects.get(id=input_serializer.data['product_id'])

        Basket.objects.get(user=request.user, product=product).delete()

        return Response()


class OrderView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_body=OrderSerializer,
        request_method='POST',
        responses={
            200: OrderSerializer
        }
    )
    def post(self, request):
        input_serializer = OrderSerializer(data=request.data, context={'request': request})
        input_serializer.is_valid(raise_exception=True)

        order = input_serializer.save()

        return Response(input_serializer.data)