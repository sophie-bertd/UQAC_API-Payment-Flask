import pytest

from orders_products import get_db, Product, ShippingInformation, CreditCard, Transaction, Order

class TestFruitsVeggies(object):
    def test_index(self, app, db, client):
        with app.app_context():
            response = client.get('/')
            assert response.status_code == 200

    def test_get_order_not_found(self, app, db, client):
        with app.app_context():
            response = client.get('/order/999')
            assert response.status_code == 404

    def test_post_order_missing_fields(self, app, db, client):
        with app.app_context():
            response = client.post('/order', json={})
            assert response.status_code == 422

    def test_post_order_invalid_product(self, app, db, client):
        with app.app_context():
            response = client.post('/order', json={"product": {"id": 999, "quantity": 1}})
            assert response.status_code == 404

    def test_post_order_out_of_stock(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=False, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            
            response = client.post('/order', json={"product": {"id": 123, "quantity": 1}})
            assert response.status_code == 422

    def test_post_order_successful(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()

            response = client.post('/order', json={"product": {"id": 123, "quantity": 1}})
            assert response.status_code == 302

    def test_put_order_invalid_order_id(self, app, db, client):
        with app.app_context():
            response = client.put('/order/999', json={})
            assert response.status_code == 404

    def test_put_order_invalid_body(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})

            response = client.put('/order/1', json={})
            assert response.status_code == 422

    def test_put_order_missing_fields(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})

            response = client.put('/order/1', json={"order": {"shipping_information": {"coutry": "", "address": "", "postal_code": "", "city": "", "province": ""}, "email": ""}})
            assert response.status_code == 422

    def test_put_order_successful(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})

            response = client.put('/order/1', json={"order": {"shipping_information": {"country": "Canada", "address": "123 rue de la pomme", "postal_code": "H0H 0H0", "city": "Pommeville", "province": "QC"}, "email": "test@example.com"}})
            assert response.status_code == 200

    def test_put_order_payment_missing_fields(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})
            client.put('/order/1', json={"order": {"shipping_information": {"country": "Canada", "address": "123 rue de la pomme", "postal_code": "H0H 0H0", "city": "Pommeville", "province": "QC"}, "email": "test@example.com"}})

            response = client.put('/order/1', json={})
            assert response.status_code == 422

    def test_put_order_payment_already_paid(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})
            client.put('/order/1', json={"order": {"shipping_information": {"country": "Canada", "address": "123 rue de la pomme", "postal_code": "H0H 0H0", "city": "Pommeville", "province": "QC"}, "email": "test@example.com"}})

            response = client.put('/order/1', json={"order": {"paid": True}})
            assert response.status_code == 422

    def test_put_order_payment_successful(self, app, db, client):
        with app.app_context():
            p = Product.create(id=123, name="Pomme", in_stock=True, description="pompom", price=1.23, weight=0.123, image="http://pomme.com")
            p.save()
            client.post('/order', json={"product": {"id": 123, "quantity": 1}})
            client.put('/order/1', json={"order": {"shipping_information": {"country": "Canada", "address": "123 rue de la pomme", "postal_code": "H0H 0H0", "city": "Pommeville", "province": "QC"}, "email": "test@example.com"}})

            response = client.put('/order/1', json={"credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2026, "expiration_month": 12, "cvv": "123"}})
            assert response.status_code == 200