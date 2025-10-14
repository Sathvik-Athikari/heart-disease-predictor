import os
import json
import joblib
import warnings
import numpy as np
import pandas as pd
import tensorflow as tf

# Cleaner logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
def _safe_lower_str(x):
    try:
        return str(x).strip()
    except Exception:
        return x

def _to_num(x, default=0):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return default
        return float(x)
    except Exception:
        return default

def _extract_feature_groups(preprocessor):
    """Extract num/cat/pass features from preprocessor"""
    num, cat, pas = [], [], []
    try:
        # sklearn ColumnTransformer stores transformers_ as tuples (name, transformer, columns)
        for name, trans, cols in preprocessor.transformers_:
            if name == "num":
                num = list(cols)
            elif name == "cat":
                cat = list(cols)
            elif name == "pass":
                pas = list(cols)
    except Exception:
        # If the preprocessor doesn't expose transformers_ in that shape, return empty sets
        pass
    return set(num), set(cat), set(pas)

def _ensure_expected_columns(df, assets, disease_name=""):
    """Aligns input dataframe with training columns"""
    expected = list(assets["columns"])
    pre = assets["preprocessor"]

    num_set, cat_set, pas_set = _extract_feature_groups(pre)
    expected_set = set(expected)
    df_cols = set(df.columns)

    missing = expected_set - df_cols
    extra = df_cols - expected_set

    if missing or extra:
        print(f"🔧 [{disease_name}] Column alignment:")
        if missing:
            print(f"   + Adding {len(missing)} missing columns:", list(missing)[:10])
        if extra:
            print(f"   - Dropping {len(extra)} extra columns:", list(extra)[:10])

    for col in missing:
        if col in cat_set:
            df[col] = "Unknown"
        else:
            df[col] = 0

    for col in expected:
        if col in cat_set:
            df[col] = df[col].astype(str).fillna("Unknown")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df[expected]

# ---------------------------------------------------------------------
# Load models
# ---------------------------------------------------------------------
def load_all_models():
    models = {}
    base_path = os.path.join(os.path.dirname(__file__), "models")
    model_names = ["stroke", "heart_failure", "hypertension", "heart_attack", "cad"]

    print("🚀 Loading models...")
    for name in model_names:
        try:
            model_dir = os.path.join(base_path, name)
            model_path = os.path.join(model_dir, f"{name}_model.keras")
            preproc_path = os.path.join(model_dir, f"{name}_preprocessor.joblib")
            cols_path = os.path.join(model_dir, f"{name}_columns.json")

            if not os.path.exists(model_dir):
                raise FileNotFoundError(f"Model directory not found: {model_dir}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not os.path.exists(preproc_path):
                raise FileNotFoundError(f"Preprocessor file not found: {preproc_path}")
            if not os.path.exists(cols_path):
                raise FileNotFoundError(f"Columns file not found: {cols_path}")

            model = tf.keras.models.load_model(model_path)
            preprocessor = joblib.load(preproc_path)
            with open(cols_path, "r") as f:
                columns = json.load(f)

            models[name] = {"model": model, "preprocessor": preprocessor, "columns": columns}
            print(f"✅ {name} loaded (features: {len(columns)})")
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
            # return None  # keep trying to load other models? we return None to indicate failure
            return None
    print("-" * 40)
    return models

# ---------------------------------------------------------------------
# Mapping helpers
# ---------------------------------------------------------------------
def _map_yes_no(v):
    v = str(v).lower().strip()
    if v in {"y", "yes", "1", "true"}: return 1
    if v in {"n", "no", "0", "false"}: return 0
    try: return int(v)
    except: return 0

def _map_sex(v):
    v = str(v).lower().strip()
    if v in {"m", "male"}: return 1
    if v in {"f", "female", "fmale"}: return 0
    return 0

# ---------------------------------------------------------------------
# Prediction functions (for each disease)
# ---------------------------------------------------------------------
def predict_stroke(patient, assets):
    df = pd.DataFrame([patient]).copy()
    if "Sex" in df:
        df["Sex"] = df["Sex"].apply(_map_sex)
    if "Age" in df:
        df["Age"] = df["Age"].apply(lambda x: int(np.ceil(_to_num(x))))
    if "Married" in df:
        df["Married"] = df["Married"].apply(lambda x: 1 if str(x).lower() in {"yes","1","true","y"} else 0)
    df.rename(columns={
        "Heart_disease":"heart_disease",
        "Glucose_level":"glucose_level",
        "Smoking_status":"smoking_status",
        "Work_type":"work_type",
        "Residence_type":"residence_type"
    }, inplace=True)
    df = _ensure_expected_columns(df, assets, "stroke")
    X = assets["preprocessor"].transform(df)
    return float(assets["model"].predict(X, verbose=0)[0][0])

def predict_heart_failure(patient, assets):
    df = pd.DataFrame([patient]).copy()
    if "Sex" in df:
        df["Sex"] = df["Sex"].apply(_map_sex)
    # keep any other renames as necessary
    df.rename(columns={
        "ChestPainType":"chest_pain_type",
        "RestingBP":"resting_bp",
        "Cholesterol":"cholesterol",
        "FastingBS":"fasting_bs",
        "RestingECG":"resting_ecg",
        "MaxHR":"max_hr",
        "ExerciseAngina":"exercise_angina",
        "Oldpeak":"oldpeak",
        "ST_Slope":"st_slope"
    }, inplace=True)
    df = _ensure_expected_columns(df, assets, "heart_failure")
    X = assets["preprocessor"].transform(df)
    return float(assets["model"].predict(X, verbose=0)[0][0])

def predict_hypertension(patient, assets):
    df = pd.DataFrame([patient]).copy()
    if "Sex" in df:
        df["sex"] = df["Sex"].apply(_map_sex)
        df.drop(columns=["Sex"], inplace=True, errors="ignore")
    if "Gender" in df:
        df["sex"] = df["Gender"].apply(_map_sex)
        df.drop(columns=["Gender"], inplace=True, errors="ignore")
    if "Diabetes" in df:
        df["diabetes"] = df["Diabetes"].apply(_map_yes_no)
        df.drop(columns=["Diabetes"], inplace=True, errors="ignore")
    if "Smoking_Status" in df:
        smap = {"Never":"never smoked","Current":"smokes","Former":"formerly smoked"}
        df["smokes"] = df["Smoking_Status"].map(smap).fillna("never smoked")
        df.drop(columns=["Smoking_Status"], inplace=True, errors="ignore")
    df = _ensure_expected_columns(df, assets, "hypertension")
    X = assets["preprocessor"].transform(df)
    return float(assets["model"].predict(X, verbose=0)[0][0])

def predict_heart_attack(patient, assets):
    df = pd.DataFrame([patient]).copy()
    drop_cols = ["Patient ID","Country","Continent","Hemisphere","Income"]
    df.drop(columns=[c for c in drop_cols if c in df], inplace=True, errors="ignore")
    if "Sex" in df:
        df["sex"] = df["Sex"].apply(_map_sex)
        df.drop(columns=["Sex"], inplace=True, errors="ignore")
    if "Gender" in df:
        df["sex"] = df["Gender"].apply(_map_sex)
        df.drop(columns=["Gender"], inplace=True, errors="ignore")
    df.rename(columns={
        "Heart rate":"heart_rate",
        "Systolic blood pressure":"systolic_bp",
        "Diastolic blood pressure":"diastolic_bp",
        "Blood sugar":"blood_sugar",
        "CK_MB":"CK-MB",
        "Troponin_level":"Troponin"
    }, inplace=True)
    df = _ensure_expected_columns(df, assets, "heart_attack")
    X = assets["preprocessor"].transform(df)
    return float(assets["model"].predict(X, verbose=0)[0][0])

def predict_cad(patient, assets):
    df = pd.DataFrame([patient]).copy()
    if "sex" in df:
        df["sex"] = df["sex"].apply(_map_sex)
    binary_cols = ["Obesity","CRF","CVA","Airway disease","Thyroid Disease",
                   "CHF","DLP","Weak Peripheral Pulse","Lung rales",
                   "Systolic Murmur","Diastolic Murmur","Dyspnea",
                   "atypical_angina","non_anginal_pain","Exertional CP",
                   "LowTH Ang","LVH","Poor R Progression"]
    for c in binary_cols:
        if c in df:
            df[c] = df[c].apply(_map_yes_no)
    df = _ensure_expected_columns(df, assets, "cad")
    X = assets["preprocessor"].transform(df)
    return float(assets["model"].predict(X, verbose=0)[0][0])

# ---------------------------------------------------------------------
# Master Input Template
# ---------------------------------------------------------------------
master_input_template = {
    "Age": 0, "Sex": "Female", "BMI": 22.0, "systolic_bp": 120, "diastolic_bp": 80,
    "cholesterol": 200, "LDL": 100, "HDL": 50, "triglycerides": 150,
    "glucose_level": 90, "Hypertension": 0, "diabetes": 0, "heart_disease": 0,
    "FH": 0, "smokes": 0, "smoking_status": "never smoked", "Troponin": 0.01,
    "CK-MB": 2.5, "heart_rate": 80, "oldpeak": 0.0
}

# ---------------------------------------------------------------------
# Module-level model cache (loaded once)
# ---------------------------------------------------------------------
MODELS = load_all_models()
if MODELS is None:
    print("❌ Warning: Models were not loaded at import time. Ensure model files exist in backend/models/*")
else:
    print("✅ Models cached in MODELS variable for fast prediction.")

# ---------------------------------------------------------------------
# Unified function for app.py
# ---------------------------------------------------------------------
def predict_all_diseases(patient_data):
    models = MODELS if MODELS is not None else load_all_models()
    if models is None:
        return {"error": "Models not loaded."}

    final_input = dict(master_input_template)
    final_input.update(patient_data)

    results = {
        "stroke": predict_stroke(final_input, models["stroke"]),
        "heart_failure": predict_heart_failure(final_input, models["heart_failure"]),
        "hypertension": predict_hypertension(final_input, models["hypertension"]),
        "heart_attack": predict_heart_attack(final_input, models["heart_attack"]),
        "cad": predict_cad(final_input, models["cad"]),
    }

    output = {}
    for disease, risk in results.items():
        pct = max(0.0, min(1.0, risk)) * 100
        level = "High" if pct > 70 else ("Moderate" if pct > 50 else "Low")
        output[disease] = {"score": round(pct, 2), "risk": level}

    return {"predictions": output}
