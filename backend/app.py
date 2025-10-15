# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from main import predict_all_diseases, load_all_models

app = Flask(__name__)
CORS(app)

# Ensure models are loaded on startup (this prints status to console)
models = load_all_models()
if models is None:
    print("❌ Warning: models not loaded at startup. Check backend/models/*")
else:
    print("✅ Models loaded at startup.")

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": bool(models)})

@app.route("/predict_all", methods=["POST"])
def predict_all():
    try:
        payload = request.get_json()
        if payload is None:
            return jsonify({"error": "No JSON body received"}), 400

        # ✅ Unwrap 'data' key if frontend sends JSON like {"data": {...}}
        if "data" in payload and isinstance(payload["data"], dict):
            payload = payload["data"]

        print("\n📥 [BACKEND] Received JSON from frontend:")
        print(json.dumps(payload, indent=2))

        result = predict_all_diseases(payload)

        print("\n✅ [BACKEND] Prediction response to frontend:")
        print(json.dumps(result, indent=2))

        return jsonify(result)

    except Exception as e:
        print("❌ Exception in /predict_all:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Debug True is fine for local testing; turn off for production
    app.run(host="0.0.0.0", port=8000, debug=True)
