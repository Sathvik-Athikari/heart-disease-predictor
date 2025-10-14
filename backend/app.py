from flask import Flask, request, jsonify
from flask_cors import CORS
from main import predict_all_diseases

app = Flask(__name__)
CORS(app)  # allow requests from frontend (React)

@app.route("/")
def home():
    return jsonify({"message": "Heart Disease Prediction API is running 🚀"})

@app.route("/predict_all", methods=["POST"])
def predict_all():
    try:
        patient_data = request.get_json()
        if not patient_data:
            return jsonify({"error": "No input JSON received"}), 400

        print("📥 Received data from frontend:", patient_data)

        result = predict_all_diseases(patient_data)
        print("✅ Prediction result:", result)

        return jsonify(result)

    except Exception as e:
        print("❌ Error in prediction:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
