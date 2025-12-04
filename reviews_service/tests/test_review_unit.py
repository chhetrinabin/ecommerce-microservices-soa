from datetime import datetime
from src.models import Review


def test_review_to_dict_serialization():
    r = Review(id=3, product_id=10, user_id=20, rating=5, comment="Great", created_at=datetime(2025,5,6,7,8,9))
    d = r.to_dict()

    assert d["id"] == 3
    assert d["product_id"] == 10
    assert d["user_id"] == 20
    assert d["rating"] == 5
    assert d["comment"] == "Great"
    assert isinstance(d["created_at"], str)
    assert d["created_at"].startswith("2025-05-06T07:08:09")
