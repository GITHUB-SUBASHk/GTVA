# app/gesture_model.py
import tensorflow as tf
import numpy as np
from .utils import extract_landmarks, rule_based_gesture

# Load pre-trained model (assumes trained on landmarks)
try:
    model = tf.keras.models.load_model("models/saved_model.h5")
except:
    model = None
    print("Warning: No model loaded. Rule-based gestures only.")

labels = ["Hello", "Yes", "No", "Thank You", "I Love You"]

def predict_gesture(image):
    """Predict gesture using rule-based logic or model-based detection."""
    img_height, img_width = image.shape[:2]
    
    # Extract landmarks
    landmarks, hand_landmarks = extract_landmarks(image)
    
    # Rule-based gesture for simple cases
    rule_gesture = rule_based_gesture(hand_landmarks, img_width, img_height)
    if rule_gesture:
        return rule_gesture
    
    # Model-based gesture for complex cases
    if model and landmarks is not None:
        landmarks = np.expand_dims(landmarks, axis=0)  # Shape: (1, 63)
        predictions = model.predict(landmarks, verbose=0)
        return labels[np.argmax(predictions)]
    
    return "No gesture detected"