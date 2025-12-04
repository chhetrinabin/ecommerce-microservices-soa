from flask import Flask, request, jsonify, abort, g
from flask_cors import CORS
from models import db, Product
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

def create_app():
    app = Flask(__name__)
    CORS(app)
    db_path = os.environ.get("DB_PATH", "/data/products.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Prometheus metrics
    REQUEST_COUNT = Counter(
        "product_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "http_status"],
    )

    REQUEST_LATENCY = Histogram(
        "product_request_latency_seconds",
        "Request latency in seconds",
        ["method", "endpoint"],
    )

    @app.before_request
    def _start_timer():
        g._start_time = time.time()

    @app.after_request
    def _observe_request(response):
        try:
            resp_time = time.time() - g._start_time
        except Exception:
            resp_time = 0.0
        endpoint = request.path
        REQUEST_LATENCY.labels(request.method, endpoint).observe(resp_time)
        REQUEST_COUNT.labels(request.method, endpoint, str(response.status_code)).inc()
        return response

    @app.route("/metrics", methods=["GET"])
    def metrics():
        # Expose Prometheus metrics
        data = generate_latest()
        return data, 200, {"Content-Type": CONTENT_TYPE_LATEST}

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "product_service"}), 200

    @app.route("/products", methods=["GET"])
    def list_products():
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products])

    @app.route("/products/<int:pid>", methods=["GET"])
    def get_product(pid):
        p = db.session.get(Product, pid)
        if p is None:
            abort(404)
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
        p = db.session.get(Product, pid)
        if p is None:
            abort(404)
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
        p = db.session.get(Product, pid)
        if p is None:
            abort(404)
        db.session.delete(p)
        db.session.commit()
        return jsonify({"deleted": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
