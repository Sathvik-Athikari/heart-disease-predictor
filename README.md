# 🫀 CardioPredict — AI-Powered Heart Disease Predictor

CardioPredict is a full-stack web application that uses **machine learning** to predict multiple heart-related diseases (Stroke, Hypertension, CAD, Heart Failure, Heart Attack, etc.) based on user health data extracted from uploaded medical reports.

---

## 🚀 Features

- 🧬 Predicts multiple cardiovascular diseases using ML models.
- 📄 Automatically extracts data from uploaded PDF medical reports.
- ✍️ Allows manual input for missing attributes.
- 👩‍⚕️ User authentication (Sign Up / Login) with secure password hashing.
- 🧠 SQLite3 database for user & prediction storage.
- 🧩 Fully functional frontend built with **React + Tailwind CSS**.
- ⚡ Backend powered by **Flask** and **scikit-learn** models.
- 🌍 Deployment-ready for **Netlify (Frontend)** + **Render (Backend)**.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React.js, Tailwind CSS, Framer Motion, Axios |
| **Backend** | Flask, Python, SQLite3, Flask-CORS |
| **ML Models** | scikit-learn |
| **Authentication** | Werkzeug Password Hashing |
| **Deployment** | Netlify (Frontend) + Render (Backend) |

---

## 📂 Project Structure

CardioPredict/
├── backend/
│ ├── app.py # Flask main backend
│ ├── main.py # ML model loading & prediction logic
│ ├── database.py # SQLite setup & helper functions
│ ├── models/ # Trained model .pkl files
│ ├── .env # Secret keys & port (not pushed to Git)
│ ├── requirements.txt # Python dependencies
│ └── users.db # Auto-created local DB
│
├── frontend/
│ ├── src/
│ │ ├── pages/ # Login, Signup, Profile, Prediction, etc.
│ │ ├── components/ # Navbar, Footer
│ │ └── App.jsx
│ └── package.json
│
└── README.md


Backend Setup 

cd backend
python -m venv venv
venv/Scripts/activate      # (Windows)
# OR
source venv/bin/activate   # (Mac/Linux)

pip install -r requirements.txt


Frontend Setup

cd ../frontend
npm install
npm run dev


.env

FLASK_SECRET_KEY=secret-key
PORT=8000
