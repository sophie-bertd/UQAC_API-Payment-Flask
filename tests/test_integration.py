import pytest

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
            response = client.post('/order', json={"product_id": 999, "quantity": 1})
            assert response.status_code == 404

    def test_post_order_out_of_stock(self, app, db, client):
        with app.app_context():
            response = client.post('/order', json={"product_id": 1, "quantity": 1})
            assert response.status_code == 422

    def test_post_order_successful(self, app, db, client):
        with app.app_context():
            response = client.post('/order', json={"product_id": 2, "quantity": 1})
            assert response.status_code == 302

    def test_put_order_invalid_order_id(self, app, db, client):
        with app.app_context():
            response = client.put('/order/999', json={"order": {"shipping_information": {}, "email": "test@example.com"}})
            assert response.status_code == 404

    def test_put_order_invalid_body(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={"invalid": "body"})
            assert response.status_code == 422

    def test_put_order_missing_fields(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={})
            assert response.status_code == 422

    def test_put_order_successful(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={"order": {"shipping_information": {"country": "Canada", "address": "123 rue de la pomme", "postal_code": "H0H 0H0", "city": "Pommeville", "province": "QC"}, "email": "test@example.com"}})
            assert response.status_code == 200

    def test_put_order_payment_missing_fields(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={})
            assert response.status_code == 422

    def test_put_order_payment_already_paid(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={"order": {"paid": True}})
            assert response.status_code == 422

    def test_put_order_payment_successful(self, app, db, client):
        with app.app_context():
            response = client.put('/order/1', json={"credit_card": {"number": "4242 4242 4242 4242", "expiration_year": 2026, "expiration_month": 12, "cvv": "123"}})
            assert response.status_code == 200