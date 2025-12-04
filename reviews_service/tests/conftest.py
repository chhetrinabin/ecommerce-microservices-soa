import os
import tempfile
import pytest

from src.app import create_app
from src.models import db


@pytest.fixture(scope="session")
def app():
    fd, db_path = tempfile.mkstemp(prefix="reviews_test_", suffix=".db")
    os.close(fd)

    os.environ["DB_PATH"] = db_path
    os.environ["FLASK_ENV"] = "testing"

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture()
def client(app):
    return app.test_client()
