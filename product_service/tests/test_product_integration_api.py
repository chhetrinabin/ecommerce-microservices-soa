def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "product_service"


def test_create_list_get_update_delete_product(client):
    # Create
    r = client.post("/products", json={"name": "Widget", "price": 4.5, "stock": 10})
    assert r.status_code == 201
    created = r.get_json()
    pid = created["id"]
    assert created["name"] == "Widget"

    # List
    r = client.get("/products")
    assert r.status_code == 200
    products = r.get_json()
    assert any(p["id"] == pid for p in products)

    # Get
    r = client.get(f"/products/{pid}")
    assert r.status_code == 200
    one = r.get_json()
    assert one["id"] == pid

    # Update (PATCH)
    r = client.patch(f"/products/{pid}", json={"name": "WidgetPro", "price": 5.0})
    assert r.status_code == 200
    updated = r.get_json()
    assert updated["name"] == "WidgetPro"
    assert float(updated["price"]) == 5.0

    # Delete
    r = client.delete(f"/products/{pid}")
    assert r.status_code == 200
    assert r.get_json()["deleted"] is True

    # Verify deleted
    r = client.get(f"/products/{pid}")
    assert r.status_code == 404
