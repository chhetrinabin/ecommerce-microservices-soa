def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "reviews_service"


def test_create_invalid_rating_returns_400(client):
    r = client.post("/reviews", json={"product_id": 1, "user_id": 1, "rating": 0})
    assert r.status_code == 400


def test_create_list_get_update_delete_review(client):
    # Create
    payload = {"product_id": 11, "user_id": 22, "rating": 4, "comment": "Nice"}
    r = client.post("/reviews", json=payload)
    assert r.status_code == 201
    created = r.get_json()
    rid = created["id"]
    assert created["rating"] == 4

    # List
    r = client.get("/reviews")
    assert r.status_code == 200
    reviews = r.get_json()
    assert any(rv["id"] == rid for rv in reviews)

    # Get
    r = client.get(f"/reviews/{rid}")
    assert r.status_code == 200

    # Update (rating out of range)
    r = client.patch(f"/reviews/{rid}", json={"rating": 6})
    assert r.status_code == 400

    # Update valid
    r = client.patch(f"/reviews/{rid}", json={"comment": "Updated", "rating": 5})
    assert r.status_code == 200
    updated = r.get_json()
    assert updated["rating"] == 5
    assert updated["comment"] == "Updated"

    # Delete
    r = client.delete(f"/reviews/{rid}")
    assert r.status_code == 200
    assert r.get_json()["deleted"] is True

    # Verify deleted
    r = client.get(f"/reviews/{rid}")
    assert r.status_code == 404
