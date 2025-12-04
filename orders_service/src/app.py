from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import db, Order, OrderItem
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    db_path = os.environ.get("DB_PATH", "/data/orders.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "orders_service"}), 200

    @app.route("/orders", methods=["GET"])
    def list_orders():
        orders = Order.query.all()
        return jsonify([o.to_dict() for o in orders])

    @app.route("/orders/<int:oid>", methods=["GET"])
    def get_order(oid):
        o = db.session.get(Order, oid)
        if o is None:
            abort(404)
        return jsonify(o.to_dict())

    @app.route("/orders", methods=["POST"])
    def create_order():
        data = request.get_json(force=True)
        user_id = data.get("user_id")
        items = data.get("items", [])  # [{product_id, quantity, price}]
        if not user_id or not isinstance(items, list) or len(items) == 0:
            return jsonify({"error": "user_id and items are required"}), 400

        order = Order(user_id=user_id, status=data.get("status", "pending"))
        for item in items:
            order.items.append(OrderItem(
                product_id=int(item["product_id"]),
                quantity=int(item.get("quantity", 1)),
                price=float(item.get("price", 0.0))
            ))
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201

    @app.route("/orders/<int:oid>", methods=["PUT", "PATCH"])
    def update_order(oid):
        o = db.session.get(Order, oid)
        if o is None:
            abort(404)
        data = request.get_json(force=True)
        if "status" in data:
            o.status = data["status"]
        if "items" in data and isinstance(data["items"], list):
            for old in list(o.items):
                db.session.delete(old)
            for item in data["items"]:
                o.items.append(OrderItem(
                    product_id=int(item["product_id"]),
                    quantity=int(item.get("quantity", 1)),
                    price=float(item.get("price", 0.0))
                ))
        db.session.commit()
        return jsonify(o.to_dict())

    @app.route("/orders/<int:oid>", methods=["DELETE"])
    def delete_order(oid):
        o = db.session.get(Order, oid)
        if o is None:
            abort(404)
        db.session.delete(o)
        db.session.commit()
        return jsonify({"deleted": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5003)))
