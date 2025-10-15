# backend/main.py
import os
import json
import joblib
import warnings
import numpy as np
import pandas as pd
import tensorflow as tf
from typing import Dict, Any

# Cleaner logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")

# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
def _to_num(x, default=0):
    try:
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return default
        return float(x)
    except Exception:
        return default

def _extract_feature_groups(preprocessor):
    """Try to extract numeric/categorical/passthrough column lists from a ColumnTransformer-like preprocessor.
    Returns sets (num_set, cat_set, pass_set). If not available, returns empty sets."""
    num, cat, pas = [], [], []
    try:
        # sklearn ColumnTransformer stores transformers_ as tuples (name, transformer, columns)
        for name, trans, cols in preprocessor.transformers_:
            name = str(name).lower()
            if name == "num":
                num = list(cols)
            elif name == "cat":
                cat = list(cols)
            elif name in {"pass", "passthrough"}:
                pas = list(cols)
    except Exception:
        # best-effort: some preprocessors may not expose .transformers_
        pass
    return set(num), set(cat), set(pas)

def _ensure_expected_columns(df: pd.DataFrame, assets: Dict[str, Any], disease_name: str = "") -> pd.DataFrame:
    """Align df to assets['columns'] with proper dtypes and default values for missing features."""
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
            print(f"   + Adding {len(missing)} missing columns: {list(missing)[:20]}")
        if extra:
            print(f"   - Dropping {len(extra)} extra columns: {list(extra)[:20]}")

    # Fill missing columns with defaults: categorical -> "Unknown", numeric -> 0
    for col in missing:
        if col in cat_set:
            df[col] = "Unknown"
        else:
            df[col] = 0

    # Enforce ordering and types
    for col in expected:
        if col in cat_set:
            df[col] = df[col].astype(str).fillna("Unknown")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df[expected]

# ---------------------------------------------------------------------
# Master Input Template (full set you provided)
# ---------------------------------------------------------------------
master_input_template = {
    "Age":0,"Sex":"Female","sex":"Female","Gender":"Female","BMI":22.0,
    "systolic_bp":120,"diastolic_bp":80,"resting_bp":120,
    "cholesterol":200,"LDL":100,"HDL":50,"triglycerides":150,
    "glucose_level":90,"blood_sugar":90,"FBS":90,
    "Hypertension":0,"diabetes":0,"heart_disease":0,
    "FH":0,"Family_History":"No",
    "smokes":0,"formerly_smoked":0,"smoking_status":"never smoked",
    "Obesity":"N","CRF":"N","CVA":"N","Airway disease":"N","Thyroid Disease":"N",
    "CHF":"N","DLP":"N","Edema":"N","Weak Peripheral Pulse":"N","Lung rales":"N",
    "Systolic Murmur":"N","Diastolic Murmur":"N","Dyspnea":"N","Function Class":0,
    "typical_angina":"N","atypical_angina":"N","non_anginal_pain":"N",
    "Exertional CP":"N","LowTH Ang":"N","Q Wave":"N","St Elevation":"N",
    "St Depression":"N","Tinversion":"N","LVH":"N","Poor R Progression":"N","BBB":"None",
    "CR":1.0,"BUN":15,"ESR":10,"HB":14.0,"K":4.0,"Na":140,"WBC":7000,
    "Lymph":30,"Neut":60,"PLT":250000,"EF-TTE":60,"Region RWMA":0,"VHD":"N",
    "ldl_hdl_ratio":3.0,
    "chest_pain_type":"NAP","resting_ecg":"Normal","max_hr":150,
    "exercise_angina":"N","oldpeak":0.0,"st_slope":"Up",
    "heart_rate":80,"CK-MB":2.5,"Troponin":0.01,
    "Married":"No","work_type":"Private","residence_type":"Urban"
}

# ---------------------------------------------------------------------
# Mapping helpers (normalize some common fields)
# ---------------------------------------------------------------------
def _map_yes_no(v):
    v = str(v).lower().strip()
    if v in {"y", "yes", "1", "true"}:
        return 1
    if v in {"n", "no", "0", "false"}:
        return 0
    try:
        return int(v)
    except Exception:
        return 0

def _map_sex(v):
    v = str(v).lower().strip()
    if v in {"m", "male"}:
        return 1
    if v in {"f", "female"}:
        return 0
    return 0

# ---------------------------------------------------------------------
# Model loading & caching (loads once)
# Directory expected: backend/models/{disease}/{disease}_model.keras, etc.
# ---------------------------------------------------------------------
MODELS = None

def load_all_models(base_path: str = None):
    global MODELS
    if MODELS is not None:
        return MODELS

    if base_path is None:
        # relative to this file directory
        base_path = os.path.join(os.path.dirname(__file__), "models")

    model_names = ["stroke", "heart_failure", "hypertension", "heart_attack", "cad"]
    models = {}

    print("🚀 Loading models from:", base_path)
    for name in model_names:
        try:
            model_dir = os.path.join(base_path, name)
            model_path = os.path.join(model_dir, f"{name}_model.keras")
            preproc_path = os.path.join(model_dir, f"{name}_preprocessor.joblib")
            cols_path = os.path.join(model_dir, f"{name}_columns.json")

            # Basic existence checks
            if not os.path.exists(model_dir):
                raise FileNotFoundError(f"Model directory not found: {model_dir}")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not os.path.exists(preproc_path):
                raise FileNotFoundError(f"Preprocessor file not found: {preproc_path}")
            if not os.path.exists(cols_path):
                raise FileNotFoundError(f"Columns file not found: {cols_path}")

            # Load
            model = tf.keras.models.load_model(model_path)
            preprocessor = joblib.load(preproc_path)
            with open(cols_path, "r") as f:
                columns = json.load(f)

            models[name] = {"model": model, "preprocessor": preprocessor, "columns": columns}
            print(f"✅ Loaded {name} (features: {len(columns)})")
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
            # Fail fast: set MODELS to None and return None
            MODELS = None
            return None

    MODELS = models
    print("-" * 40)
    return MODELS

# Attempt to load at import time (so Flask startup is immediate)
load_all_models()

# ---------------------------------------------------------------------
# Generic prediction helper (applies necessary renames and mappings)
# ---------------------------------------------------------------------
def _prepare_dataframe_for_model(patient: Dict[str, Any], assets: Dict[str, Any], disease_name: str) -> pd.DataFrame:
    """Return a dataframe aligned with model columns, after light normalization."""
    df = pd.DataFrame([patient]).copy()

    # Common normalizations
    # Map Sex / Gender -> numeric 'sex' or 'Sex' depending on what models expect
    if "Sex" in df:
        try:
            df["Sex"] = df["Sex"].apply(_map_sex)
        except Exception:
            pass
    if "Gender" in df and "Sex" not in df:
        try:
            df["Gender"] = df["Gender"].apply(_map_sex)
        except Exception:
            pass

    # Map common boolean-like fields
    for col in ["Hypertension", "diabetes", "heart_disease"]:
        if col in df:
            df[col] = df[col].apply(_map_yes_no)

    # Some pipelines expect lowercased column names or slightly different names.
    # Implement per-disease renames if you used them during training (examples below).
    # Add renames used in your training pipelines if needed:
    rename_map = {
        # heart_attack used "CK-MB" sometimes
        "CK_MB": "CK-MB",
        "Troponin_level": "Troponin",
        "Heart rate": "heart_rate",
        "Systolic blood pressure": "systolic_bp",
        "Diastolic blood pressure": "diastolic_bp",
        "ChestPainType": "chest_pain_type",
        "RestingBP": "resting_bp",
        "FastingBS": "fasting_bs",
        "RestingECG": "resting_ecg",
        "MaxHR": "max_hr",
        "ExerciseAngina": "exercise_angina",
        "Oldpeak": "oldpeak",
        "ST_Slope": "st_slope",
        "Heart_disease": "heart_disease",
        "Glucose_level": "glucose_level",
        "Smoking_status": "smoking_status"
    }
    for a, b in rename_map.items():
        if a in df.columns and b not in df.columns:
            df.rename(columns={a: b}, inplace=True)

    # Align and typecast according to model assets
    df_aligned = _ensure_expected_columns(df, assets, disease_name)
    return df_aligned

def predict_disease(patient: Dict[str, Any], assets: Dict[str, Any], disease_name: str) -> float:
    """Prepare input, log it, run preprocessor + model, return probability [0,1]."""
    df_pre = _prepare_dataframe_for_model(patient, assets, disease_name)

    # Log the input that will be fed into the model
    try:
        print(f"\n🧪 [{disease_name.upper()}] Input sent to model:")
        print(df_pre.head(1).to_dict(orient="records")[0])
    except Exception:
        print(f"🧪 [{disease_name.upper()}] (could not print input)")

    # Transform and predict
    X = assets["preprocessor"].transform(df_pre)
    pred = float(assets["model"].predict(X, verbose=0)[0][0])
    print(f"🔢 [{disease_name.upper()}] Model raw output: {pred}")
    return pred

# ---------------------------------------------------------------------
# Public API: predict_all_diseases()
# ---------------------------------------------------------------------
def predict_all_diseases(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main entrypoint for Flask app. 
    Merges frontend data with master_input_template (defaults)."""
    models = MODELS if MODELS is not None else load_all_models()
    if models is None:
        return {"error": "Models not loaded. Ensure backend/models/* exists and is correct."}

    # ✅ Deep copy of master template
    final_input = dict(master_input_template)

    # ✅ Override defaults with frontend values (only if key exists in master_input_template)
    if isinstance(patient_data, dict):
        for key, value in patient_data.items():
            if key in final_input:
                final_input[key] = value
            else:
                # Ignore unknown keys safely
                pass
    else:
        return {"error": "Invalid input format (expected JSON object)"}

    print("\n🧾 [MERGED FINAL INPUT] Sent to models:")
    for k, v in list(final_input.items())[:15]:
        print(f"   {k}: {v}")
    if len(final_input) > 15:
        print(f"   ... ({len(final_input)} total keys)")

    # ✅ Predict with each model
    predictions = {}
    for disease_name, assets in models.items():
        try:
            prob = predict_disease(final_input, assets, disease_name)
            pct = round(float(prob) * 100, 2)
            level = "High" if pct > 70 else ("Moderate" if pct > 50 else "Low")
            predictions[disease_name] = {"score": float(pct), "risk": level}
        except Exception as e:
            print(f"❌ Error predicting {disease_name}: {e}")
            predictions[disease_name] = {"error": str(e)}

    return {"predictions": predictions}
