# Gesture Communication Web App

This application provides real-time gesture recognition for communication, particularly for the hearing/speech impaired, using MediaPipe for hand landmark detection and a TensorFlow model for gesture classification. It supports both rule-based and model-based gesture recognition, with a web interface for webcam streaming and image uploads.

## Features
- Real-time gesture recognition via webcam using MediaPipe and TensorFlow.
- Supports simple gestures (e.g., Pinch, Fist) via rule-based logic.
- Supports complex gestures (e.g., Hello, Yes, No) via a trained model.
- Web interface for live video and static image uploads.
- Data collection and model training scripts for custom gestures.

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project_root