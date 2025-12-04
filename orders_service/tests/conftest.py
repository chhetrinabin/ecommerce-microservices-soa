import os
import sys
import tempfile
import pathlib
import pytest

# Ensure the service's `src/` directory is on sys.path when pytest runs from repository root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent.joinpath('src')))

from app import create_app
from models import db


@pytest.fixture(scope="session")
def app():
    fd, db_path = tempfile.mkstemp(prefix="orders_test_", suffix=".db")
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
