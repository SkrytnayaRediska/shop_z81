import pytest
from rest_framework.test import APITestCase, APIClient
from django.shortcuts import reverse
from conftest import EVERYTHING_EQUALS_NON_NONE

pytestmark = [pytest.mark.django_db]


class ClientEndpointsTestCase(APITestCase):
    fixtures = [
        'catalog/tests/fixtures/categories_fixture.json',
        'catalog/tests/fixtures/discounts_fixture.json',
        'catalog/tests/fixtures/producers_fixture.json',
        'catalog/tests/fixtures/products_fixture.json'
    ]

    def test_categories_list(self):
        url = reverse('categories')
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert response.data == [
            {
                "id": 1,
                "name": EVERYTHING_EQUALS_NON_NONE,
                "description": EVERYTHING_EQUALS_NON_NONE
            },
            {
                "id": 2,
                "name": EVERYTHING_EQUALS_NON_NONE,
                "description": EVERYTHING_EQUALS_NON_NONE
            },
            {
                "id": 3,
                "name": EVERYTHING_EQUALS_NON_NONE,
                "description": EVERYTHING_EQUALS_NON_NONE
            },
        ]

    def test_category_by_id(self):
        url = reverse('category-products', kwargs={"category_id": 1})
        response = self.client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert response.data == [
            {
                "id": 1,
                "name": EVERYTHING_EQUALS_NON_NONE,
                "price": "100.00",
                "count_on_stock": EVERYTHING_EQUALS_NON_NONE,
                "articul": EVERYTHING_EQUALS_NON_NONE,
                "description": EVERYTHING_EQUALS_NON_NONE,
                "discount": EVERYTHING_EQUALS_NON_NONE,
                "producer": EVERYTHING_EQUALS_NON_NONE,
                "category": EVERYTHING_EQUALS_NON_NONE
            }
        ]

        assert response.data[0]["discount"] == {
            "id": 1,
            "name": EVERYTHING_EQUALS_NON_NONE,
            "percent": EVERYTHING_EQUALS_NON_NONE,
            "date_start": EVERYTHING_EQUALS_NON_NONE,
            "date_end": EVERYTHING_EQUALS_NON_NONE
        }

        assert response.data[0]["producer"] == {
            "id": 1,
            "name": EVERYTHING_EQUALS_NON_NONE,
            "description": EVERYTHING_EQUALS_NON_NONE,
            "country": EVERYTHING_EQUALS_NON_NONE
        }

        assert response.data[0]["category"] == {
            "id": 1,
            "name": EVERYTHING_EQUALS_NON_NONE,
            "description": EVERYTHING_EQUALS_NON_NONE
        }
