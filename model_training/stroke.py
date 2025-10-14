# --- 0. INSTALL REQUIRED LIBRARIES ---
# In Google Colab, imblearn is usually pre-installed. If not, run:
# !pip install imbalanced-learn

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
    # If running in Google Colab, upload 'Stroke1.csv' to your session storage first.
    df = pd.read_csv('Stroke1.csv')
    print("✅ File 'Stroke1.csv' loaded successfully.")
except FileNotFoundError:
    print("❌ Error: Could not find 'Stroke1.csv'. Please upload it to your Colab session.")
    exit()

# --- 2. DATA CLEANING & STANDARDIZATION ---
print("\nCleaning and standardizing data...")
# Rule 1: Remove the ID column
if 'ID' in df.columns:
    df.drop('ID', axis=1, inplace=True)

# Rule 2: Convert 'Sex' to binary (1 for Male, 0 for Female) and handle 'Other'
if 'Other' in df['Sex'].unique():
    df = df[df['Sex'] != 'Other']
df['Sex'] = df['Sex'].apply(lambda x: 1 if x == 'Male' else 0)

# Rule 3: Convert 'Age' to whole numbers using ceiling
df['Age'] = df['Age'].apply(lambda x: int(np.ceil(x)))

# Rule 4: Convert 'Married' to binary (1 for Yes, 0 for No)
df['Married'] = df['Married'].apply(lambda x: 1 if x == 'Yes' else 0)

# Standardize column names for consistency
df.rename(columns={
    'Heart_disease': 'heart_disease', 'Glucose_level': 'glucose_level',
    'Smoking_status': 'smoking_status', 'Work_type': 'work_type',
    'Residence_type': 'residence_type', 'Target': 'target'
}, inplace=True)
print("✅ Data cleaning complete.")

# --- 3. PREPROCESSING PIPELINE ---
X = df.drop('target', axis=1)
y = df['target']

numerical_features = ['Age', 'glucose_level', 'BMI']
categorical_features = ['work_type', 'residence_type', 'smoking_status']
passthrough_features = [col for col in X.columns if col not in numerical_features + categorical_features]

numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
])

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

# --- 5. APPLY SMOTE TO HANDLE CLASS IMBALANCE ---
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_processed, y_train)
print(f"✅ SMOTE applied. New class distribution: {np.bincount(y_train_resampled)}")

# --- 6. BUILD A STRONG DNN MODEL ---
# This model is deeper and uses advanced techniques to prevent overfitting.
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train_resampled.shape[1],)),

    # Layer 1: Wider first layer with L2 regularization
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.5),

    # Layer 2: Middle layer
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.4),

    # Layer 3: Final hidden layer
    tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.3),

    # Output Layer
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ]
)

model.summary()

# --- 7. DEFINE CALLBACKS FOR SMART TRAINING ---
# These will stop training when performance stops improving and adjust the learning rate.
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=15, # Number of epochs with no improvement after which training will be stopped.
    restore_best_weights=True # Restores model weights from the epoch with the best value of the monitored quantity.
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2, # Factor by which the learning rate will be reduced. new_lr = lr * factor
    patience=5,
    min_lr=0.00001
)

# --- 8. TRAIN THE MODEL ---
print("\n🚀 Starting advanced model training...")
history = model.fit(
    X_train_resampled,
    y_train_resampled,
    epochs=200, # Train for more epochs; EarlyStopping will find the best one
    batch_size=32,
    validation_data=(X_test_processed, y_test),
    callbacks=[early_stopping, reduce_lr],
    verbose=1 # Set to 1 to see the training progress
)
print("\n✅ Model training complete.")

# --- 9. FINAL EVALUATION ---
print("\n🔬 Evaluating final model on test data...")
results = model.evaluate(X_test_processed, y_test)

print("\n--- FINAL MODEL PERFORMANCE ---")
print(f"   Test Loss: {results[0]:.4f}")
print(f"   Test Accuracy: {results[1]*100:.2f}%")
print(f"   Test Precision: {results[2]:.4f}")
print(f"   Test Recall: {results[3]:.4f}")
print("---------------------------------")
print("Precision: Of all the patients the model predicted would have a stroke, how many actually did.")
print("Recall: Of all the patients who actually had a stroke, how many did the model correctly identify.")
