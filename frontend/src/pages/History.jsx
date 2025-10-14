import React from "react";
import { motion } from "framer-motion";

const History = () => {
  // Example data — later this will come from backend
  const pastPredictions = [
    {
      id: 1,
      date: "2025-09-01",
      disease: "Coronary Artery Disease",
      risk: "High",
    },
    {
      id: 2,
      date: "2025-08-15",
      disease: "Heart Attack",
      risk: "Moderate",
    },
    {
      id: 3,
      date: "2025-07-30",
      disease: "Hypertensive Heart Disease",
      risk: "Low",
    },
    {
      id: 4,
      date: "2025-07-10",
      disease: "Stroke",
      risk: "Moderate",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 px-6 py-10 pt-24">
      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-4xl font-bold text-center text-blue-600 mb-10"
      >
        Prediction History
      </motion.h1>

      {/* Table */}
      <div className="max-w-5xl mx-auto bg-white shadow-lg rounded-xl overflow-hidden border border-gray-200">
        <table className="w-full border-collapse">
          <thead className="bg-blue-100 text-blue-700">
            <tr>
              <th className="p-4 text-left">#</th>
              <th className="p-4 text-left">Date</th>
              <th className="p-4 text-left">Disease Predicted</th>
              <th className="p-4 text-left">Risk Level</th>
            </tr>
          </thead>
          <tbody>
            {pastPredictions.map((prediction, index) => (
              <motion.tr
                key={prediction.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="border-b hover:bg-blue-50 transition"
              >
                <td className="p-4 font-medium">{index + 1}</td>
                <td className="p-4">{prediction.date}</td>
                <td className="p-4">{prediction.disease}</td>
                <td
                  className={`p-4 font-semibold ${
                    prediction.risk === "High"
                      ? "text-red-600"
                      : prediction.risk === "Moderate"
                      ? "text-yellow-600"
                      : "text-green-600"
                  }`}
                >
                  {prediction.risk}
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;
