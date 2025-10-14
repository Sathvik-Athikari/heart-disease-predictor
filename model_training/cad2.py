# --- 0. INSTALL REQUIRED LIBRARIES ---
# In Google Colab, imblearn is usually pre-installed. If not, run:
# !pip install imblearn

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

print("TensorFlow Version:", tf.__version__)

# --- 1. DATA LOADING ---
try:
    df = pd.read_csv('CAD.csv')
    print("✅ File 'CAD.csv' loaded successfully.")
except FileNotFoundError:
    print("❌ Error: Could not find 'CAD.csv'. Please upload it to your Colab session.")
    exit()

# --- 2. DATA CLEANING & STANDARDIZATION ---
print("\nCleaning and standardizing data...")

# Rule 1: Handle the Target Variable
df['Cath'] = df['Cath'].apply(lambda x: 1 if x == 'Cad' else 0)
df.rename(columns={'Cath': 'target'}, inplace=True)
print(f"✅ Target variable 'Cath' processed. Distribution:\n{df['target'].value_counts()}")

# Rule 2: Standardize Column Names
df.rename(columns={
    'DM': 'diabetes', 'HTN': 'hypertension', 'Current Smoker': 'smokes',
    'EX-Smoker': 'formerly_smoked', 'BP': 'systolic_bp', 'PR': 'heart_rate',
    'Typical Chest Pain': 'typical_angina', 'Atypical': 'atypical_angina',
    'Nonanginal': 'non_anginal_pain', 'TG': 'triglycerides', 'Sex': 'sex'
}, inplace=True)

# Rule 3: Drop Redundant Columns
df.drop(columns=['Weight', 'Length'], inplace=True)

# Rule 4: Clean and Convert Binary Features
# Define a mapping for all 'Y'/'N' and 'Male'/'Fmale' style columns
binary_map = {'Y': 1, 'N': 0, 'Male': 1, 'Fmale': 0}
binary_cols = [
    'sex', 'Obesity', 'CRF', 'CVA', 'Airway disease', 'Thyroid Disease',
    'CHF', 'DLP', 'Weak Peripheral Pulse', 'Lung rales', 'Systolic Murmur',
    'Diastolic Murmur', 'Dyspnea', 'atypical_angina', 'non_anginal_pain',
    'Exertional CP', 'LowTH Ang', 'LVH', 'Poor R Progression'
]
for col in binary_cols:
    df[col] = df[col].map(binary_map)

# Rule 5: Feature Engineering
# Create a more powerful cholesterol ratio feature
df['ldl_hdl_ratio'] = df['LDL'] / (df['HDL'] + 1e-6)
print("✅ Feature engineering complete: 'ldl_hdl_ratio' created.")

# Rule 6: Handle specific missing values or placeholders if any (e.g., in 'BBB')
df['BBB'] = df['BBB'].replace('N', 'None') # Assuming 'N' means no block

# --- 3. PREPROCESSING PIPELINE ---
X = df.drop('target', axis=1)
y = df['target']

# Define feature types for the pipeline
numerical_features = [
    'Age', 'BMI', 'systolic_bp', 'heart_rate', 'Function Class', 'FBS', 'CR',
    'triglycerides', 'LDL', 'HDL', 'BUN', 'ESR', 'HB', 'K', 'Na', 'WBC',
    'Lymph', 'Neut', 'PLT', 'EF-TTE', 'Region RWMA', 'ldl_hdl_ratio'
]
categorical_features = ['VHD', 'BBB']
# All other columns are already cleaned to 0/1 and can be passed through
passthrough_features = [col for col in X.columns if col not in numerical_features + categorical_features]

# Create transformers
numerical_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))])

# Create the master preprocessor
preprocessor = ColumnTransformer(transformers=[
    ('num', numerical_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features),
    ('pass', 'passthrough', passthrough_features)
])

# --- 4. DATA SPLITTING & PREPROCESSING ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)
print(f"\n✅ Data preprocessed. Original class distribution in training set: {np.bincount(y_train)}")

# --- 5. APPLY SMOTE ---
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_processed, y_train)
print(f"✅ SMOTE applied. New class distribution: {np.bincount(y_train_resampled)}")

# --- 6. BUILD A STRONG DNN MODEL ---
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train_resampled.shape[1],)),
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')]
)
model.summary()

# --- 7. DEFINE CALLBACKS & TRAIN ---
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=7, min_lr=0.00001)

print("\n🚀 Starting advanced model training...")
history = model.fit(
    X_train_resampled, y_train_resampled,
    epochs=200, batch_size=16, # Smaller batch size for this smaller dataset
    validation_data=(X_test_processed, y_test),
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)
print("\n✅ Model training complete.")

# --- 8. FINAL EVALUATION ---
print("\n🔬 Evaluating final model on test data...")
results = model.evaluate(X_test_processed, y_test)

print("\n--- FINAL MODEL PERFORMANCE ---")
print(f"   Test Loss: {results[0]:.4f}")
print(f"   Test Accuracy: {results[1]*100:.2f}%")
print(f"   Test Precision: {results[2]:.4f}")
print(f"   Test Recall: {results[3]:.4f}")
print("---------------------------------")
