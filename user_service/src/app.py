from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    db_path = os.environ.get("DB_PATH", "/data/users.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "user_service"}), 200

    @app.route("/users", methods=["GET"])
    def list_users():
        users = list(User.query.all())
        return jsonify([u.to_dict() for u in users])

    @app.route("/users/<int:uid>", methods=["GET"])
    def get_user(uid):
        u = User.query.get_or_404(uid)
        return jsonify(u.to_dict())

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json(force=True)
        u = User(name=data.get("name"), email=data.get("email"))
        db.session.add(u)
        db.session.commit()
        return jsonify(u.to_dict()), 201

    @app.route("/users/<int:uid>", methods=["PUT", "PATCH"])
    def update_user(uid):
        u = User.query.get_or_404(uid)
        data = request.get_json(force=True)
        if "name" in data:
            u.name = data["name"]
        if "email" in data:
            u.email = data["email"]
        db.session.commit()
        return jsonify(u.to_dict())

    @app.route("/users/<int:uid>", methods=["DELETE"])
    def delete_user(uid):
        u = User.query.get_or_404(uid)
        db.session.delete(u)
        db.session.commit()
        return jsonify({"deleted": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))
