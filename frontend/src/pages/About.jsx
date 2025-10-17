import { motion } from "framer-motion";

const diseases = [
  {
    name: "Coronary Artery Disease",
    image: "/images/coronary.png", // replace with actual image
    description:
      "Coronary Artery Disease occurs when major blood vessels supplying the heart become damaged or blocked due to plaque buildup.",
    causes: ["High cholesterol", "Smoking", "High blood pressure"],
    params: ["Age", "Cholesterol levels", "Blood pressure", "ECG"],
  },
  {
    name: "Heart Failure",
    image: "/images/heart_failure.png",
    description:
      "Heart failure occurs when the heart cannot pump blood effectively, leading to fatigue and fluid buildup.",
    causes: ["Diabetes", "Obesity", "High blood pressure"],
    params: ["Age", "Ejection fraction", "Serum creatinine", "BP"],
  },
  {
    name: "Heart Attack",
    image: "/images/heart_attack.png",
    description:
      "A heart attack happens when blood flow to a part of the heart is blocked, usually by a clot in the coronary arteries.",
    causes: ["Blocked arteries", "Smoking", "Stress"],
    params: ["ECG results", "Cholesterol levels", "Blood sugar"],
  },
  {
    name: "Stroke",
    image: "/images/stroke.png",
    description:
      "A stroke occurs when blood supply to part of the brain is interrupted or reduced, depriving brain tissue of oxygen.",
    causes: ["Blood clots", "High BP", "Unhealthy lifestyle"],
    params: ["BP", "Glucose levels", "Age", "Smoking status"],
  },
  {
    name: "Hypertensive Heart Disease",
    image: "/images/hypertension.png",
    description:
      "This disease develops due to long-term high blood pressure, causing the heart to work harder and weaken over time.",
    causes: ["Prolonged high BP", "Obesity", "Smoking"],
    params: ["BP", "BMI", "Family history"],
  },
];

const About = () => {
  return (
    <div className="min-h-screen bg-white text-gray-800 px-8 py-12 pt-28">
      {/* Heading */}
      <motion.h1
        className="text-4xl font-bold text-center text-blue-600 mb-12"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        About Our AI Model
      </motion.h1>

      {/* Model Info */}
      <motion.p
        className="text-lg leading-relaxed text-center max-w-3xl mx-auto mb-12"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.8 }}
      >
        Our AI model uses a deep neural network trained on medical datasets with
        an accuracy of <span className="font-bold text-blue-500">92%</span>. It
        predicts the risks of five major heart diseases by analyzing patient
        health parameters. The results are displayed as{" "}
        <span className="font-bold text-red-500">Low, Moderate, or High risk</span>.
      </motion.p>

      {/* Disease Sections */}
      <div className="space-y-16 max-w-6xl mx-auto">
        {diseases.map((disease, index) => (
          <motion.div
            key={index}
            className="flex flex-col md:flex-row items-center gap-8"
            initial={{ opacity: 0, x: index % 2 === 0 ? -100 : 100 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            {/* Image */}
            <img
              src={disease.image}
              alt={disease.name}
              className="w-[250px] h-[250px] object-contain rounded-xl shadow-md"
            />

            {/* Text Info */}
            <div className="flex-1">
              <h2 className="text-2xl font-semibold text-blue-600 mb-4">
                {disease.name}
              </h2>
              <p className="text-gray-700 mb-3">{disease.description}</p>
              <p className="text-gray-700 mb-2">
                <span className="font-bold">Causes:</span>{" "}
                {disease.causes.join(", ")}.
              </p>
              <p className="text-gray-700">
                <span className="font-bold">Parameters:</span>{" "}
                {disease.params.join(", ")}.
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default About;
