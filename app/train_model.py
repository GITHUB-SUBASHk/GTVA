# app/train_model.py
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

def train_model(data_dir="data", output_model="models/saved_model.h5"):
    """Train a TensorFlow model on gesture landmark data."""
    # Load all gesture CSV files
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        print("Error: No gesture data found in", data_dir)
        return
    
    data = pd.concat([pd.read_csv(os.path.join(data_dir, f)) for f in csv_files])
    X = data.drop('label', axis=1).values
    y = LabelEncoder().fit_transform(data['label'])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(len(set(y)), activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=20, validation_split=0.2, batch_size=32)
    
    # Evaluate model
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {test_acc:.4f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    model.save(output_model)
    print(f"Model saved to {output_model}")

if __name__ == "__main__":
    train_model()