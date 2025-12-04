from flask_sqlalchemy import SQLAlchemy
from src.models import Product, db


def test_db_is_sqlalchemy_instance():
    assert isinstance(db, SQLAlchemy)


def test_product_table_and_columns():
    assert Product.__tablename__ == "products"
    cols = {c.name for c in Product.__table__.columns}
    expected = {"id", "name", "description", "price", "stock", "created_at"}
    assert expected.issubset(cols)
