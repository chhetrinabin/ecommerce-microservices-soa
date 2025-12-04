from datetime import datetime
from src.models import Order, OrderItem


def test_order_to_dict_and_total():
    o = Order(id=1, user_id=10, status="pending", created_at=datetime(2025,1,2,3,4,5))
    # attach items
    i1 = OrderItem(id=1, product_id=100, quantity=2, price=5.0)
    i2 = OrderItem(id=2, product_id=101, quantity=1, price=3.5)
    # SQLAlchemy relationship not required for unit-level calculation; set list directly
    o.items = [i1, i2]

    d = o.to_dict()
    assert d["id"] == 1
    assert d["user_id"] == 10
    assert d["status"] == "pending"
    assert isinstance(d["created_at"], str)
    assert isinstance(d["items"], list)
    assert d["total"] == 2*5.0 + 1*3.5
