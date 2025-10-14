import React, { useState } from "react";
import axios from "axios";
import * as pdfjsLib from "pdfjs-dist/webpack"; // ✅ worker handled automatically

const Prediction = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [missingFields, setMissingFields] = useState([]);
  const [manualInputs, setManualInputs] = useState({});
  const [parsedFeatures, setParsedFeatures] = useState({});

  // ✅ Required attributes from your PDF file
  const REQUIRED_COLUMNS = {
    stroke: ["Age", "heart_disease", "Married", "BMI", "Hypertension", "glucose_level", "Sex", "smoking_status"],
    hypertension: ["systolic_bp", "BP_Medications", "diastolic_bp", "sex", "diabetes", "heart_rate", "BMI", "glucose_level", "Age", "cigsPerDay", "cholesterol", "smokes"],
    heart_failure: ["oldpeak", "cholesterol", "max_hr", "Sex", "resting_bp", "fasting_bs", "Age", "Chest_pain_type", "Resting_ecg", "Fasting_bs", "St_slope"],
    heart_attack: ["Troponin", "CK_MB", "sex", "systolic_bp", "blood_sugar", "diastolic_bp", "heart_rate", "Age"],
    cad: ["typical_angina", "Region", "RWMA", "K", "Age", "EF-TTE", "systolic_bp", "hypertension", "FH", "heart_rate", "Tinversion", "HDL", "ESR", "Lymph", "HB", "WBC", "Weight", "CR", "BMI", "triglycerides", "FBS", "diabetes", "Na", "LDL", "PLT", "smokes", "BUN", "Neut", "sex", "Length"]
  };

  const handleFileChange = (e) => setFile(e.target.files[0]);

  // ✅ Extract text from PDF
  const extractTextFromPDF = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let textContent = "";

    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const text = await page.getTextContent();
      text.items.forEach((item) => (textContent += item.str + " "));
    }
    return textContent;
  };

  // 🔹 Parse extracted text into JSON
  const parsePDFtoJSON = async (file) => {
    const text = await extractTextFromPDF(file);
    console.log("📄 Extracted PDF Text:", text);

    const parsed = {};

    // Combine all required features into one big list
    const allFeatures = [
      ...new Set(Object.values(REQUIRED_COLUMNS).flat())
    ];

    allFeatures.forEach((feature) => {
      const regex = new RegExp(`${feature}\\s*[:\\-]?\\s*([A-Za-z0-9\\.]+)`, "i");
      const match = text.match(regex);
      if (match) {
        let value = match[1];
        if (!isNaN(value)) value = parseFloat(value);
        parsed[feature] = value;
      }
    });
    console.log("✅ Parsed Features:", parsed);
    return parsed;
  };

  // Manual input change handler
  const handleInputChange = (e, field) => {
    setManualInputs({ ...manualInputs, [field]: e.target.value });
  };

  // 🔍 Check for missing fields BEFORE backend call
  const checkMissingFields = (parsed) => {
    const allRequired = new Set(Object.values(REQUIRED_COLUMNS).flat());
    const missing = [...allRequired].filter((col) => !(col in parsed));
    return missing;
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF report before uploading.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // 1️⃣ Extract + parse PDF
      const parsed = await parsePDFtoJSON(file);
      console.log("🧠 Final Extracted Data to Send Backend:", parsed);

      setParsedFeatures(parsed);

      // 2️⃣ Check for missing fields
      const missing = checkMissingFields(parsed);

      if (missing.length > 0) {
        setMissingFields(missing);
        setError("Some required fields are missing. Please fill them manually below.");
        setLoading(false);
        return;
      }

      // 3️⃣ No missing fields — send to backend
      await sendToBackend(parsed);

    } catch (err) {
      console.error(err);
      setError("Error reading the report file.");
      setLoading(false);
    }
  };

  // ✅ Combine manual inputs and send final data
  const handleManualSubmit = async () => {
    const completeData = { ...parsedFeatures, ...manualInputs };
    const stillMissing = checkMissingFields(completeData);

    if (stillMissing.length > 0) {
      setError("Please fill in all required fields before submitting.");
      return;
    }

    setError("");
    setMissingFields([]);
    setLoading(true);
    await sendToBackend(completeData);
  };

  const sendToBackend = async (data) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/predict", // ✅ Flask endpoint
        { data }
      );
      setResults(response.data.predictions);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Backend error during prediction.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ Color for risk visualization
  const getColor = (riskLevel) => {
    if (!riskLevel) return "#9E9E9E";
    if (riskLevel < 33) return "#4CAF50";
    if (riskLevel < 66) return "#FFC107";
    return "#F44336";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex flex-col items-center pt-24 px-4">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl">
        <h2 className="text-2xl font-bold text-center mb-6 text-blue-600">
          Upload Report for Prediction
        </h2>

        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="mb-4 block w-full border rounded-lg p-2"
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          {loading ? "Processing..." : "Upload & Predict"}
        </button>

        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
      </div>

      {/* Missing input fields */}
      {missingFields.length > 0 && (
        <div className="mt-6 bg-white p-6 rounded-xl shadow-lg w-full max-w-2xl">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">
            Please provide missing fields:
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {missingFields.map((field) => (
              <div key={field}>
                <label className="block text-sm font-medium text-gray-600">
                  {field}
                </label>
                <input
                  type="text"
                  onChange={(e) => handleInputChange(e, field)}
                  className="mt-1 block w-full rounded-lg border px-3 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            ))}
          </div>
          <button
            onClick={handleManualSubmit}
            className="mt-4 w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition"
          >
            Submit Missing Fields
          </button>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
          {Object.entries(results).map(([disease, score]) => (
            <div
              key={disease}
              className="bg-white p-6 rounded-xl shadow-md border-l-8"
              style={{ borderLeftColor: getColor(score) }}
            >
              <h3 className="text-lg font-semibold text-gray-700 capitalize">{disease}</h3>
              <p className="text-gray-900 font-bold">
                Risk Score:{" "}
                <span style={{ color: getColor(score) }}>{score.toFixed(2)}%</span>
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Prediction;
