import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)


def get_submissions_collection():
    collection_name = os.getenv("MONGODB_COLLECTION", "submissions")
    return get_db()[collection_name]


_mongo_client = None


def get_mongo_client():
    global _mongo_client
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise ValueError("MONGODB_URI is not set. Add it to your .env file.")
    if _mongo_client is None:
        _mongo_client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    return _mongo_client


def get_db():
    db_name = os.getenv("MONGODB_DB", "flask_app")
    return get_mongo_client()[db_name]


def check_db_connection():
    """Ping MongoDB and return connection status."""
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        db = get_db()
        return {
            "ok": True,
            "database": db.name,
            "collections": db.list_collection_names(),
        }
    except (PyMongoError, ValueError) as exc:
        return {"ok": False, "error": str(exc)}


@app.route("/health/db", methods=["GET"])
def health_db():
    status = check_db_connection()
    return jsonify(status), 200 if status["ok"] else 503


@app.route("/api", methods=["GET"])
def api():
    try:
        submissions = []
        for doc in get_submissions_collection().find().sort("_id", -1):
            doc["_id"] = str(doc["_id"])
            submissions.append(doc)
        return jsonify(submissions)
    except (PyMongoError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email:
            error = "Name and email are required."
        else:
            try:
                get_submissions_collection().insert_one(
                    {
                        "name": name,
                        "email": email,
                        "message": message,
                    }
                )
                return redirect(url_for("success"))
            except (PyMongoError, ValueError) as exc:
                error = str(exc)

    return render_template("index.html", error=error)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    status = check_db_connection()
    if status["ok"]:
        print(f"MongoDB connected: {status['database']}")
    else:
        print(f"MongoDB connection failed: {status['error']}")
    app.run(debug=True, port=5000)
