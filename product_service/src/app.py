from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Product
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    db_path = os.environ.get("DB_PATH", "/data/products.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "product_service"}), 200

    @app.route("/products", methods=["GET"])
    def list_products():
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])

    @app.route("/products/<int:pid>", methods=["GET"])
    def get_product(pid):
        p = Product.query.get_or_404(pid)
        return jsonify(p.to_dict())

    @app.route("/products", methods=["POST"])
    def create_product():
        data = request.get_json(force=True)
        p = Product(
            name=data.get("name"),
            description=data.get("description", ""),
            price=float(data.get("price", 0)),
            stock=int(data.get("stock", 0))
        )
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict()), 201

    @app.route("/products/<int:pid>", methods=["PUT", "PATCH"])
    def update_product(pid):
        p = Product.query.get_or_404(pid)
        data = request.get_json(force=True)
        for field in ["name", "description"]:
            if field in data:
                setattr(p, field, data[field])
        if "price" in data:
            p.price = float(data["price"])
        if "stock" in data:
            p.stock = int(data["stock"])
        db.session.commit()
        return jsonify(p.to_dict())

    @app.route("/products/<int:pid>", methods=["DELETE"])
    def delete_product(pid):
        p = Product.query.get_or_404(pid)
        db.session.delete(p)
        db.session.commit()
        return jsonify({"deleted": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
