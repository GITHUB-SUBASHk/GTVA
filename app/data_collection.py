# app/data_collection.py
import cv2
import csv
import os
from .utils import extract_landmarks

def collect_gesture_data(gesture_name, num_samples=100, output_dir="data"):
    """Collect landmark data for a specific gesture."""
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/{gesture_name}.csv"
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = [f"lm_{i}_{coord}" for i in range(21) for coord in ['x', 'y', 'z']] + ['label']
        writer.writerow(header)
        
        frame_count = 0
        print(f"Collecting {num_samples} samples for '{gesture_name}'. Press 'q' to stop early.")
        while frame_count < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            landmarks, hand_landmarks = extract_landmarks(frame)
            if landmarks is not None:
                landmarks = landmarks.tolist()
                landmarks.append(gesture_name)
                writer.writerow(landmarks)
                frame_count += 1
                # Draw landmarks for feedback
                if hand_landmarks:
                    mp_drawing = mp.solutions.drawing_utils
                    mp_hands = mp.solutions.hands
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, f"Samples: {frame_count}/{num_samples}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f"Collecting: {gesture_name}", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"Saved {frame_count} samples to {output_file}")

if __name__ == "__main__":
    gesture = input("Enter gesture name (e.g., Hello): ")
    collect_gesture_data(gesture)