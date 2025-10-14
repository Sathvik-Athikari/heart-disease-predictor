# --- 0. INSTALL AND IMPORT LIBRARIES ---
# The 'imblearn' library is used for handling imbalanced datasets.
# It's usually pre-installed in Google Colab. If not, uncomment the line below.
# !pip install imblearn

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

print("TensorFlow Version:", tf.__version__)

# --- 1. DATA LOADING ---
try:
    # Load the new dataset.
    # If in Google Colab, make sure to upload 'Hypertension-risk-model-main.csv'.
    df = pd.read_csv('Hypertension-risk-model-main.csv')
    print("✅ File 'Hypertension-risk-model-main.csv' loaded successfully.")
    print("Initial columns:", df.columns.tolist())
except FileNotFoundError:
    print("❌ Error: Could not find 'Hypertension-risk-model-main.csv'. Please upload it to your session.")
    exit()

# --- 2. DATA CLEANING & STANDARDIZATION ---
print("\nCleaning and standardizing data as per your instructions...")

# Rule 1: Rename columns for consistency and clarity.
df.rename(columns={
    'male': 'sex',
    'age': 'Age',
    'currentSmoker': 'smokes',
    'BPMeds': 'BP_Medications',
    'totChol': 'cholesterol',
    'sysBP': 'systolic_bp',
    'diaBP': 'diastolic_bp',
    'heartRate': 'heart_rate',
    'glucose': 'glucose_level',
    'Risk': 'target'
}, inplace=True)
print("✅ Columns renamed.")
print("New columns:", df.columns.tolist())

# Rule 2: Handle Missing Values (NA)
# For numerical columns, we use the median to avoid issues with outliers.
for col in ['cigsPerDay', 'cholesterol', 'BMI', 'heart_rate', 'glucose_level']:
    if col in df.columns:
        median_val = df[col].median()
        df[col].fillna(median_val, inplace=True)
        print(f"✅ NA values in '{col}' filled with median value: {median_val}")

# For the binary 'BP_Medications' column, we use the mode (most frequent value).
if 'BP_Medications' in df.columns:
    mode_val = df['BP_Medications'].mode()[0]
    df['BP_Medications'].fillna(mode_val, inplace=True)
    print(f"✅ NA values in 'BP_Medications' filled with mode value: {mode_val}")

print("✅ Data cleaning and standardization complete.")

# --- 3. PREPROCESSING AND DATA SPLITTING ---
# Define the features (X) and the target (y)
X = df.drop('target', axis=1)
y = df['target']

# Split the data into training and testing sets before any scaling.
# 'stratify=y' ensures both sets have a similar proportion of positive/negative cases.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- 4. SCALING NUMERICAL FEATURES ---
# Scaling is crucial for DNNs to ensure all features contribute equally.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\n✅ Data scaled. Shape of scaled training data: {X_train_scaled.shape}")
print(f"Original class distribution in training set: {np.bincount(y_train)}")

# --- 5. HANDLE CLASS IMBALANCE WITH SMOTE ---
# SMOTE creates synthetic samples of the minority class to balance the dataset.
# This helps the model learn from both classes equally, improving recall.
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
print(f"✅ SMOTE applied. New class distribution: {np.bincount(y_train_resampled)}")

# --- 6. BUILD AN ADVANCED DNN MODEL WITH BATCH NORMALIZATION ---
# This architecture is robust and designed for high performance on tabular data.
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train_resampled.shape[1],)),

    # Hidden Layer 1
    tf.keras.layers.Dense(128, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(), # Normalize the activations of the previous layer
    tf.keras.layers.Activation('relu'),   # Apply activation function after normalization
    tf.keras.layers.Dropout(0.5),         # Apply dropout for regularization

    # Hidden Layer 2
    tf.keras.layers.Dense(64, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.4),

    # Hidden Layer 3
    tf.keras.layers.Dense(32, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.3),

    # Output Layer
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(name='precision'), tf.keras.metrics.Recall(name='recall')]
)

model.summary()

# --- 7. DEFINE CALLBACKS FOR SMART TRAINING ---
# EarlyStopping stops training when performance on the validation set stops improving.
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)
# ReduceLROnPlateau lowers the learning rate if the model gets stuck.
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=7,
    min_lr=0.00001
)

# --- 8. TRAIN THE MODEL ---
print("\n🚀 Starting advanced model training...")
history = model.fit(
    X_train_resampled,
    y_train_resampled,
    epochs=200,
    batch_size=32,
    validation_data=(X_test_scaled, y_test),
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)
print("\n✅ Model training complete.")

# --- 9. FINAL EVALUATION ON UNSEEN TEST DATA ---
print("\n🔬 Evaluating final model on test data...")
results = model.evaluate(X_test_scaled, y_test, verbose=0)

print("\n--- FINAL MODEL PERFORMANCE ---")
print(f"  Test Loss: {results[0]:.4f}")
print(f"  Test Accuracy: {results[1]*100:.2f}%")
print(f"  Test Precision: {results[2]:.4f}")
print(f"  Test Recall: {results[3]:.4f}")
print("---------------------------------")



#model
# --- 10. SAVE THE MODEL AND PREPROCESSOR ---
import joblib
import json

print("\n💾 Saving model and preprocessing objects...")

# 1. Save the trained TensorFlow/Keras model
model_filename = 'hypertension_model.keras'
model.save(model_filename)
print(f"✅ Model saved successfully as '{model_filename}'")

# 2. Save the StandardScaler object (the preprocessor)
preprocessor_filename = 'hypertension_preprocessor.joblib'
joblib.dump(scaler, preprocessor_filename)
print(f"✅ Preprocessor saved successfully as '{preprocessor_filename}'")

# 3. Save the list of feature column names
# This is crucial to ensure the input for prediction has the same order.
columns_filename = 'hypertension_columns.json'
with open(columns_filename, 'w') as f:
    json.dump(X.columns.tolist(), f)
print(f"✅ Feature columns saved successfully as '{columns_filename}'")

print("\nAll artifacts saved.")
