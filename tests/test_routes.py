import unittest
from decimal import Decimal
from urllib.parse import quote_plus
from service import app
from service.common import status
from service.models import db, Product
from tests.factories import ProductFactory

BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True

    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            Product.query.delete(); db.session.commit()

    def tearDown(self):
        with app.app_context(): db.session.remove()

    def _create_products(self, count=1):
        products = []
        for _ in range(count):
            product = ProductFactory()
            response = self.client.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            product.id = response.get_json()["id"]
            products.append(product)
        return products

    def test_get_product(self):
        product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["name"], product.name)

    def test_update_product(self):
        product = ProductFactory()
        response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json(); data["description"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{data['id']}", json=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["description"], "unknown")

    def test_delete_product(self):
        products = self._create_products(5)
        response = self.client.delete(f"{BASE_URL}/{products[0].id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{BASE_URL}/{products[0].id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_list(self):
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), 5)

    def test_query_by_name(self):
        products = self._create_products(5); name = products[0].name
        count = len([p for p in products if p.name == name])
        response = self.client.get(BASE_URL, query_string=f"name={quote_plus(name)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json(); self.assertEqual(len(data), count)
        for product in data: self.assertEqual(product["name"], name)

    def test_query_by_category(self):
        products = self._create_products(10); category = products[0].category
        count = len([p for p in products if p.category == category])
        response = self.client.get(BASE_URL, query_string=f"category={category.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json(); self.assertEqual(len(data), count)
        for product in data: self.assertEqual(product["category"], category.name)

    def test_query_by_availability(self):
        products = self._create_products(10)
        count = len([p for p in products if p.available is True])
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json(); self.assertEqual(len(data), count)
        for product in data: self.assertTrue(product["available"])
