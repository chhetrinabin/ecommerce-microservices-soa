from flask_sqlalchemy import SQLAlchemy
from src.models import Order, OrderItem, db


def test_db_is_sqlalchemy_instance():
    assert isinstance(db, SQLAlchemy)


def test_order_table_and_columns():
    assert Order.__tablename__ == "orders"
    cols = {c.name for c in Order.__table__.columns}
    expected = {"id", "user_id", "status", "created_at"}
    assert expected.issubset(cols)


def test_orderitem_table_and_columns():
    assert OrderItem.__tablename__ == "order_items"
    cols = {c.name for c in OrderItem.__table__.columns}
    expected = {"id", "order_id", "product_id", "quantity", "price"}
    assert expected.issubset(cols)
