# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import json
import traceback
from datetime import datetime
from main import predict_all_diseases, load_all_models
from database import get_db_connection, init_db

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# -------------------------
# Flask setup
# -------------------------
app = Flask(__name__)
CORS(app)

# ✅ Secure secret key from environment (.env)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

# -------------------------
# Initialize Database
# -------------------------
init_db()

# -------------------------
# Load ML models
# -------------------------
models = load_all_models()
if models is None:
    print("❌ Warning: models not loaded at startup. Check backend/models/*")
else:
    print("✅ Models loaded at startup.")

# -------------------------
# Health route
# -------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": bool(models)})

# -------------------------
# SIGNUP route
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return jsonify({"error": "All fields required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "User already exists"}), 409

        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
            (email, username, hashed_pw),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Signup successful!"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# -------------------------
# LOGIN route
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not all([email, password]):
            return jsonify({"error": "Email and password required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        username = user["username"]

        return jsonify({
            "message": "Login successful",
            "username": username,
            "email": email
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# -------------------------
# PREDICT_ALL route
# -------------------------
@app.route("/predict_all", methods=["POST"])
def predict_all():
    try:
        payload = request.get_json()
        if payload is None:
            return jsonify({"error": "No JSON body received"}), 400

        user_email = payload.get("email")

        # unwrap { "data": {...} }
        if "data" in payload and isinstance(payload["data"], dict):
            payload = payload["data"]

        print("\n📥 [BACKEND] Received JSON from frontend:")
        print(json.dumps(payload, indent=2))

        result = predict_all_diseases(payload)

        print("\n✅ [BACKEND] Prediction response to frontend:")
        print(json.dumps(result, indent=2))

        # ✅ Store predictions in DB
        if user_email:
            conn = get_db_connection()
            cursor = conn.cursor()
            for disease, data in result["predictions"].items():
                cursor.execute('''
                    INSERT INTO predictions (email, disease_name, score, risk)
                    VALUES (?, ?, ?, ?)
                ''', (user_email, disease, data["score"], data["risk"]))
            conn.commit()
            conn.close()

        return jsonify(result)

    except Exception as e:
        print("❌ Exception in /predict_all:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
