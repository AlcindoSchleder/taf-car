# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.urls import reverse


class TestLengthConversion(TestCase):
    """
    This class contains tests to all calls to the api that supply carriers module.
    """
    END_POINTS = {
        'all_products': '/tafApi/product/1.0/{p1}',
        'fractional_products': '/tafApi/product/1.0/fractional/{p1}',
        'greatness_products': '/tafApi/product/1.0/greatness/{p1}',
        'product': '/tafApi/product/1.0/%d',
        'product-image': '/tafAPI/product/1.0/pk/%s'
    }

    def setUp(self):
        """
        This method runs before the execution of each test case.
        """
        self.client = Client()
        self.url = reverse("carriers:carriers")

    def test_show_page(self):
        """
        Tests show page with parameters.
        """
        pass

    def test_call_all_products_api(self):
        """
        Tests call to all products api.
        """
        data = {
            "end_points": self.END_POINTS,
            "api_name": "all_products",
            "params": {
                "pk_last_charge": 0
            },
        }
        response = self.client.get(self.url, data)
        self.assertContains(response, 80.969)
