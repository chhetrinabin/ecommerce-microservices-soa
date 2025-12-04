def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "orders_service"


def test_create_list_get_update_delete_order(client):
    # Create - missing fields => 400
    r = client.post("/orders", json={})
    assert r.status_code == 400

    # Create valid order
    payload = {"user_id": 5, "items": [{"product_id": 1, "quantity": 2, "price": 3.0}]}
    r = client.post("/orders", json=payload)
    assert r.status_code == 201
    created = r.get_json()
    oid = created["id"]
    assert created["user_id"] == 5
    assert isinstance(created["items"], list)
    assert created["total"] == 6.0

    # List
    r = client.get("/orders")
    assert r.status_code == 200
    orders = r.get_json()
    assert any(o["id"] == oid for o in orders)

    # Get
    r = client.get(f"/orders/{oid}")
    assert r.status_code == 200

    # Update status
    r = client.patch(f"/orders/{oid}", json={"status": "shipped"})
    assert r.status_code == 200
    updated = r.get_json()
    assert updated["status"] == "shipped"

    # Update items (replace)
    r = client.patch(f"/orders/{oid}", json={"items": [{"product_id": 2, "quantity": 1, "price": 10.0}]})
    assert r.status_code == 200
    updated = r.get_json()
    assert updated["total"] == 10.0

    # Delete
    r = client.delete(f"/orders/{oid}")
    assert r.status_code == 200
    assert r.get_json()["deleted"] is True

    # Verify deleted
    r = client.get(f"/orders/{oid}")
    assert r.status_code == 404
