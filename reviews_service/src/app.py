from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from .models import db, Review
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    db_path = os.environ.get("DB_PATH", "/data/reviews.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "reviews_service"}), 200

    @app.route("/reviews", methods=["GET"])
    def list_reviews():
        product_id = request.args.get("product_id")
        user_id = request.args.get("user_id")
        q = Review.query
        if product_id:
            q = q.filter_by(product_id=int(product_id))
        if user_id:
            q = q.filter_by(user_id=int(user_id))
        return jsonify([r.to_dict() for r in q.all()])

    @app.route("/reviews/<int:rid>", methods=["GET"])
    def get_review(rid):
        r = db.session.get(Review, rid)
        if r is None:
            abort(404)
        return jsonify(r.to_dict())

    @app.route("/reviews", methods=["POST"])
    def create_review():
        data = request.get_json(force=True)
        rating = int(data.get("rating", 0))
        if rating < 1 or rating > 5:
            return jsonify({"error": "rating must be 1..5"}), 400
        r = Review(
            product_id=int(data.get("product_id")),
            user_id=int(data.get("user_id")),
            rating=rating,
            comment=data.get("comment", ""),
        )
        db.session.add(r)
        db.session.commit()
        return jsonify(r.to_dict()), 201

    @app.route("/reviews/<int:rid>", methods=["PUT", "PATCH"])
    def update_review(rid):
        r = db.session.get(Review, rid)
        if r is None:
            abort(404)
        data = request.get_json(force=True)
        if "comment" in data:
            r.comment = data["comment"]
        if "rating" in data:
            rating = int(data["rating"])
            if rating < 1 or rating > 5:
                return jsonify({"error": "rating must be 1..5"}), 400
            r.rating = rating
        db.session.commit()
        return jsonify(r.to_dict())

    @app.route("/reviews/<int:rid>", methods=["DELETE"])
    def delete_review(rid):
        r = db.session.get(Review, rid)
        if r is None:
            abort(404)
        db.session.delete(r)
        db.session.commit()
        return jsonify({"deleted": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5004)))
