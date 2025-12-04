from flask_sqlalchemy import SQLAlchemy
from src.models import User, db


def test_db_is_sqlalchemy_instance():
    assert isinstance(db, SQLAlchemy)


def test_user_table_and_columns():
    # Verify the declarative mapping metadata
    assert User.__tablename__ == "users"
    cols = {c.name for c in User.__table__.columns}
    expected = {"id", "name", "email", "created_at"}
    assert expected.issubset(cols)
