import pytest

from orders_products import Product, ShippingInformation, CreditCard, Transaction, Order

class TestProduct(object):
    def test_init(self):
        p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
        assert p.id == 123
        assert p.name == "Pomme"
        assert p.in_stock == True
        assert p.description == "pompom"
        assert p.price == 1.23
        assert p.weight == 0.123
        assert p.image == "http://pomme.com"

class TestShippingInformation(object):
    def test_init(self):
        s = ShippingInformation(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
        assert s.country == "Canada"
        assert s.address == "123 rue de la pomme"
        assert s.postal_code == "H0H 0H0"
        assert s.city == "Pommeville"
        assert s.province == "QC"

class TestCreditCard(object):
    def test_init(self):
        c = CreditCard(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
        assert c.name == "Pomme"
        assert c.number == "1234567890"
        assert c.expiration_year == 2020
        assert c.expiration_month == 12
        assert c.cvv == "123"

class TestTransaction(object):
    def test_init(self):
        t = Transaction(id="123", success=True, amount_charged=1.23)
        assert t.id == "123"
        assert t.success == True
        assert t.amount_charged == 1.23

class TestOrder(object):
    def test_init(self):
        p = Product(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
        s = ShippingInformation(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
        c = CreditCard(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
        t = Transaction(id="123", success=True, amount_charged=1.23)
        o = Order(id=123, total_price=42.24, email="order@gmail.com", paid=True, shipping_price=2.99, product_id=p.id, quantity=1, shipping_information=s, credit_card=c, transaction=t)
        assert o.id == 123
        assert o.total_price == 42.24
        assert o.email == "order@gmail.com"
        assert o.paid == True
        assert o.shipping_price == 2.99
        assert o.product_id == 123
        assert o.quantity == 1
        assert o.shipping_information == s
        assert o.credit_card == c
        assert o.transaction == t