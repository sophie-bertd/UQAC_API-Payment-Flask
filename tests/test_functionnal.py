import pytest

from orders_products import get_db, Product, ShippingInformation, CreditCard, Transaction, Order

class TestProduct(object):
    def test_init(self):
        with app.app_context():
            p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()

            new_product = get_db().execute("SELECT id, name, in_stock, description, price, weight, image_url FROM products WHERE id = ?", [123]).fetchone()
            assert new_product[0] == 123
            assert new_product[1] == "Pomme"
            assert new_product[2] == 1
            assert new_product[3] == "pompom"
            assert new_product[4] == 1.23
            assert new_product[5] == 0.123
            assert new_product[6] == "http://pomme.com"

    def test_get_products(self, app):
        with app.app_context():
            p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            p = Product(id=124, name="Poire", in_stock=True, description="poipoipoi", price=1.24, weight=0.124, image="http://poire.com")
            p.save()
            p = Product(id=125, name="Banane", in_stock=True, description="babanab", price=1.25, weight=0.125, image="http://banane.com")
            p.save()

            products = Product.get_products()
            assert len(products) == 3
            assert products[0].name == "Pomme"
            assert products[1].name == "Poire"
            assert products[2].name == "Banane"

    def test_get_product_by_id(self, app):
        with app.app_context():
            p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            p = Product(id=124, name="Poire", in_stock=True, description="poipoipoi", price=1.24, weight=0.124, image="http://poire.com")
            p.save()
            p = Product(id=125, name="Banane", in_stock=True, description="babanab", price=1.25, weight=0.125, image="http://banane.com")
            p.save()

            product = Product.get_product_by_id(124)
            assert product.name == "Poire"
            product = Product.get_product_by_id(125)
            assert product.name == "Banane"
            product = Product.get_product_by_id(123)
            assert product.name == "Pomme"

class TestShippingInformation(object):
    def test_init(self):
        while app.app_context():
            s = ShippingInformation(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()

            new_shipping_information = get_db().execute("SELECT country, address, postal_code, city, province FROM shipping_information WHERE id = ?", [1]).fetchone()
            assert new_shipping_information[0] == "Canada"
            assert new_shipping_information[1] == "123 rue de la pomme"
            assert new_shipping_information[2] == "H0H 0H0"
            assert new_shipping_information[3] == "Pommeville"
            assert new_shipping_information[4] == "QC"

class TestCreditCard(object):
    def test_init(self):
        with app.app_context():
            c = CreditCard(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()

            new_credit_card = get_db().execute("SELECT name, number, expiration_year, expiration_month, cvv FROM credit_card WHERE id = ?", [1]).fetchone()
            assert new_credit_card[0] == "Pomme"
            assert new_credit_card[1] == "1234567890"
            assert new_credit_card[2] == 2020
            assert new_credit_card[3] == 12
            assert new_credit_card[4] == "123"

class TestTransaction(object):
    def test_init(self):
        with app.app_context():
            t = Transaction(id="123", success=True, amount_charged=1.23)
            t.save()

            new_transaction = get_db().execute("SELECT id, success, amount_charged FROM transaction WHERE id = ?", ["123"]).fetchone()
            assert new_transaction[0] == "123"
            assert new_transaction[1] == 1
            assert new_transaction[2] == 1.23

class TestOrder(object):
    def test_init(self):
        with app.app_context():
            p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            s = ShippingInformation(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()
            c = CreditCard(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()
            t = Transaction(id="123", success=True, amount_charged=1.23)
            t.save()
            o = Order(id=123, total_price=42.24, email="order@gmail.com", paid=True, shipping_price=2.99, product_id=p, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()

            new_order = get_db().execute("SELECT id, total_price, email, paid, shipping_price, product_id, quantity, shipping_information, credit_card, transaction FROM orders WHERE id = ?", [123]).fetchone()
            assert new_order[0] == 123
            assert new_order[1] == 42.24
            assert new_order[2] == "order@gmail.com"
            assert new_order[3] == 1
            assert new_order[4] == 2.99
            assert new_order[5] == 123
            assert new_order[6] == 1
            assert new_order[7] == s
            assert new_order[8] == c
            assert new_order[9] == t

    def test_get_order_by_id(self, app):
        with app.app_context():
            p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            s = ShippingInformation(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()
            c = CreditCard(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()
            t = Transaction(id="123", success=True, amount_charged=1.23)
            t.save()
            o = Order(id=123, total_price=42.24, email="order@gmail.com", paid=True, shipping_price=2.99, product_id=p, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()
            o = Order(id=124, total_price=42.24, email="order2@gmail.com", paid=True, shipping_price=2.99, product_id=p, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()
            o = Order(id=125, total_price=42.24, email="order3@gmail.com", paid=True, shipping_price=2.99, product_id=p, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()

            order = Order.get_order_by_id(124)
            assert order.product.name == "Pomme"
            order = Order.get_order_by_id(125)
            assert order.product.name == "Pomme"
            order = Order.get_order_by_id(123)
            assert order.product.name == "Pomme"
