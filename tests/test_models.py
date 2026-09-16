import unittest
from service import app
from service.models import Product, Category, db
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True

    def setUp(self):
        with app.app_context():
            Product.query.delete()
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()

    def test_read_a_product(self):
        product = ProductFactory(); product.id = None; product.create()
        found = Product.find(product.id)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)

    def test_update_a_product(self):
        product = ProductFactory(); product.id = None; product.create()
        original_id = product.id
        product.description = "testing"
        product.update()
        found = Product.find(original_id)
        self.assertEqual(found.id, original_id)
        self.assertEqual(found.description, "testing")

    def test_delete_a_product(self):
        product = ProductFactory(); product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        self.assertEqual(Product.all(), [])
        for _ in range(5):
            product = ProductFactory(); product.create()
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        products = ProductFactory.create_batch(10)
        for product in products: product.create()
        name = products[0].name
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), len([p for p in products if p.name == name]))
        for product in found: self.assertEqual(product.name, name)

    def test_find_by_category(self):
        products = ProductFactory.create_batch(10)
        for product in products: product.create()
        category = products[0].category
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), len([p for p in products if p.category == category]))
        for product in found: self.assertEqual(product.category, category)

    def test_find_by_availability(self):
        products = ProductFactory.create_batch(10)
        for product in products: product.create()
        available = products[0].available
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), len([p for p in products if p.available == available]))
        for product in found: self.assertEqual(product.available, available)
