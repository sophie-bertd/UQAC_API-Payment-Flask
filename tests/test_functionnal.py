import pytest

from orders_products import get_db, Product, ShippingInformation, CreditCard, Transaction, Order

class TestProduct(object):
    def test_init(self, app, db):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()

            new_product = Product.get(id=123)
            assert new_product.id == 123
            assert new_product.name == "Pomme"
            assert new_product.in_stock == True
            assert new_product.description == "pompom"
            assert float(new_product.price) == 1.23
            assert float(new_product.weight) == 0.123
            assert new_product.image == "http://pomme.com"

    def test_get_products(self, app, db):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            p = Product.create(id=124, name="Poire", in_stock=True, description="poipoipoi", price=1.24, weight=0.124, image="http://poire.com")
            p.save()
            p = Product.create(id=125, name="Banane", in_stock=True, description="babanab", price=1.25, weight=0.125, image="http://banane.com")
            p.save()

            products = Product.get_products()
            assert len(products) == 3
            assert products[0]["id"] == 123
            assert products[1]["id"] == 124
            assert products[2]["id"] == 125

    def test_get_product_by_id(self, app, db):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            p = Product.create(id=124, name="Poire", in_stock=True, description="poipoipoi", price=1.24, weight=0.124, image="http://poire.com")
            p.save()
            p = Product.create(id=125, name="Banane", in_stock=True, description="babanab", price=1.25, weight=0.125, image="http://banane.com")
            p.save()

            product = Product.get_product_by_id(124)
            assert product.id == 124
            product = Product.get_product_by_id(125)
            assert product.id == 125
            product = Product.get_product_by_id(123)
            assert product.id == 123

class TestShippingInformation(object):
    def test_init(self, app, db):
        with app.app_context():
            s = ShippingInformation.create(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()

            new_shipping_information = ShippingInformation.get(country="Canada")
            assert new_shipping_information.country == "Canada"
            assert new_shipping_information.address == "123 rue de la pomme"
            assert new_shipping_information.postal_code == "H0H 0H0"
            assert new_shipping_information.city == "Pommeville"
            assert new_shipping_information.province == "QC"

class TestCreditCard(object):
    def test_init(self, app, db):
        with app.app_context():
            c = CreditCard.create(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()

            new_credit_card = CreditCard.get(name="Pomme")
            assert new_credit_card.name == "Pomme"
            assert new_credit_card.number == "1234567890"
            assert new_credit_card.expiration_year == 2020
            assert new_credit_card.expiration_month == 12
            assert new_credit_card.cvv == "123"

class TestTransaction(object):
    def test_init(self, app, db):
        with app.app_context():
            t = Transaction.create(id="123", success=True, amount_charged=1.23)
            t.save()

            new_transaction = Transaction.get(id="123")
            assert new_transaction.id == "123"
            assert new_transaction.success == True
            assert float(new_transaction.amount_charged) == 1.23

class TestOrder(object):
    def test_init(self, app, db):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            s = ShippingInformation.create(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()
            c = CreditCard.create(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()
            t = Transaction.create(id="123", success=True, amount_charged=1.23)
            t.save()
            o = Order.create(id=123, total_price=42.24, email="order@gmail.com", paid=True, shipping_price=2.99, product_id=p.id, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()

            new_order = Order.get(id=123)
            assert new_order.id == 123
            assert float(new_order.total_price) == 42.24
            assert new_order.email == "order@gmail.com"
            assert new_order.paid == True
            assert float(new_order.shipping_price) == 2.99
            assert new_order.product_id.id == 123
            assert new_order.quantity == 1
            assert new_order.shipping_information == s
            assert new_order.credit_card == c
            assert new_order.transaction == t

    def test_get_order_by_id(self, app, db):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            s = ShippingInformation.create(country="Canada", address="123 rue de la pomme", postal_code="H0H 0H0", city="Pommeville", province="QC")
            s.save()
            c = CreditCard.create(name="Pomme", number="1234567890", expiration_year=2020, expiration_month=12, cvv="123")
            c.save()
            t = Transaction.create(id="123", success=True, amount_charged=1.23)
            t.save()
            o = Order.create(id=123, total_price=42.24, email="order@gmail.com", paid=True, shipping_price=2.99, product_id=p.id, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()
            o = Order.create(id=124, total_price=42.24, email="order2@gmail.com", paid=True, shipping_price=2.99, product_id=p.id, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()
            o = Order.create(id=125, total_price=42.24, email="order3@gmail.com", paid=True, shipping_price=2.99, product_id=p.id, quantity=1, shipping_information=s, credit_card=c, transaction=t)
            o.save()

            order = Order.get_order_by_id(124)
            assert order["id"] == 124
            order = Order.get_order_by_id(125)
            assert order["id"] == 125
            order = Order.get_order_by_id(123)
            assert order["id"] == 123
