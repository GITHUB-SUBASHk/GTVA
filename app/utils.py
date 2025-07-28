# app/utils.py
import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def extract_landmarks(image):
    """Extract normalized hand landmarks from an image using MediaPipe."""
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = []
        wrist = hand_landmarks.landmark[0]
        for lm in hand_landmarks.landmark:
            landmarks.extend([
                lm.x - wrist.x,
                lm.y - wrist.y,
                lm.z - wrist.z
            ])
        return np.array(landmarks), hand_landmarks
    return None, None

def calculate_distance(lm1, lm2, img_width, img_height):
    """Calculate Euclidean distance between two landmarks."""
    x1, y1 = lm1.x * img_width, lm1.y * img_height
    x2, y2 = lm2.x * img_width, lm2.y * img_height
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def rule_based_gesture(hand_landmarks, img_width, img_height):
    """Define simple gestures using rule-based logic."""
    if not hand_landmarks:
        return None
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    pinch_dist = calculate_distance(thumb_tip, index_tip, img_width, img_height)
    if pinch_dist < 30:
        return "Pinch"
    
    # Fist gesture: all fingertips below MCP joints
    fingertips = [8, 12, 16, 20]  # Index, middle, ring, pinky tips
    mcps = [5, 9, 13, 17]  # Corresponding MCP joints
    is_fist = True
    for tip, mcp in zip(fingertips, mcps):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y:
            is_fist = False
            break
    if is_fist:
        return "Fist"
    
    return None