from django.urls import path
from catalog.views import ProducersListView, ProducerProductsView, DiscountsListView, \
    PromocodesListView, ProductsListView, CategoriesListView, CategoryProductsView, DiscountProductsView, \
    BasketView


urlpatterns = [

    # ----- client views ------
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category-products'),

    path('producers/', ProducersListView.as_view(), name='producers'),
    path('producers/<int:producer_id>/', ProducerProductsView.as_view(), name='producer-products'),

    path('discounts/', DiscountsListView.as_view(), name='discounts'),
    path('discounts/<int:discount_id>/', DiscountProductsView.as_view(), name='discounts-products'),

    path('promocodes/', PromocodesListView.as_view(), name='promocodes'),
    path('products/', ProductsListView.as_view(), name='products'),

    # ----- customers views -----
    path('cart/', BasketView.as_view(), name='user-basket'),

]
