import os
import tempfile
import pytest
from peewee import SqliteDatabase
from orders_products import create_app
from orders_products.models import init_db, get_db, Product, ShippingInformation, CreditCard, Transaction, Order

with open(os.path.join(os.path.dirname(__file__), "../instance/database.sqlite"), "rb") as f:
    _data_sql = f.read()

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})
    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def db():
    test_db = SqliteDatabase(":memory:")
    test_db.bind([Product, ShippingInformation, CreditCard, Transaction, Order])
    test_db.connect()
    test_db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order])

    test_db.begin()

    yield test_db

    try:
        test_db.rollback()
    except Exception as e:
        print("Error during rollback:", e)
    finally:
        test_db.close()