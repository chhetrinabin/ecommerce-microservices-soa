from datetime import datetime
from src.models import Product


def test_product_to_dict_fields_and_types():
    p = Product(id=7, name="Gizmo", description="A gadget", price=9.99, stock=5, created_at=datetime(2025,6,7,8,9,10))
    d = p.to_dict()

    assert d["id"] == 7
    assert d["name"] == "Gizmo"
    assert d["description"] == "A gadget"
    assert isinstance(d["price"], float)
    assert d["price"] == 9.99
    assert d["stock"] == 5
    assert isinstance(d["created_at"], str)
    assert d["created_at"].startswith("2025-06-07T08:09:10")
