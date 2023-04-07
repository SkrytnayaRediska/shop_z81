from django.urls import path
from catalog.views import ProducersListView, ProducerProductsView, DiscountsListView, \
    PromocodesListView, ProductsListView, CategoriesListView, CategoryProductsView, DiscountProductsView

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category-products'),

    path('producers/', ProducersListView.as_view(), name='producers'),
    path('producers/<int:producer_id>/', ProducerProductsView.as_view(), name='producer-products'),

    path('discounts/', DiscountsListView.as_view(), name='discounts'),
    path('discounts/<int:discount_id>/', DiscountProductsView.as_view(), name='discounts-products'),

    path('promocodes/', PromocodesListView.as_view()),
    path('products/', ProductsListView.as_view()),
]
