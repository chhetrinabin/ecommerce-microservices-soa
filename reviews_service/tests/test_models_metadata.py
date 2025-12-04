from flask_sqlalchemy import SQLAlchemy
from src.models import Review, db


def test_db_is_sqlalchemy_instance():
    assert isinstance(db, SQLAlchemy)


def test_review_table_and_columns():
    assert Review.__tablename__ == "reviews"
    cols = {c.name for c in Review.__table__.columns}
    expected = {"id", "product_id", "user_id", "rating", "comment", "created_at"}
    assert expected.issubset(cols)
