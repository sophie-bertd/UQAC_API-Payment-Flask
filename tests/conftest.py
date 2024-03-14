import os
import tempfile

import pytest

from orders_products import create_app
from orders_products.models import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), "../instance/database.sqlite"), "rb") as f:
    _data_sql = f.read().decode("utf8")

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

@pytest.fixture
def firefox_options(request, firefox_options):
    firefox_options.add_argument('--headless')
    return firefox_options
