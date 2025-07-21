import * as handPoseDetection from '@tensorflow-models/hand-pose-detection';
import { Camera } from '@mediapipe/camera_utils';

const gestureText = document.getElementById("gesture");
const statusDiv = document.getElementById("status");
const video = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
let currentAudio = null;
let lastGesture = "";
let cooldown = false;
let detector;

const gestureMap = {
    'Open_Palm': 'Hello',
    'Fist': 'Stop',
    'Thumbs_Up': 'Good job',
    'Peace': 'Peace',
    'OK': 'Okay'
};

async function loadModel() {
    detector = await handPoseDetection.createDetector(handPoseDetection.SupportedModels.MediaPipeHands, {
        runtime: 'tfjs',
        modelType: 'lite',
        maxHands: 1
    });
    updateStatus("Model loaded");
}

function updateStatus(msg) {
    statusDiv.textContent = msg;
}

function drawLandmarks(landmarks) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    if (!landmarks) return;
    landmarks.forEach(point => {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = "cyan";
        ctx.fill();
    });
}

function classifyGesture(landmarks) {
    if (!landmarks || landmarks.length === 0) return null;
    return 'Open_Palm'; // Placeholder: Replace with your logic
}

function speakGesture(text) {
    if (cooldown || text === lastGesture) return;
    lastGesture = text;
    cooldown = true;

    fetch("/speak", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gesture: text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.audio_url) {
            if (currentAudio) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
            }
            currentAudio = new Audio(window.location.origin + data.audio_url);
            currentAudio.play();
            updateStatus(`Playing: ${text}`);
        }
        setTimeout(() => { cooldown = false; }, 4000);
    })
    .catch(() => updateStatus("Speak API error"));
}

async function detectLoop() {
    if (!detector) return;

    const hands = await detector.estimateHands(video, { flipHorizontal: true });
    if (hands.length > 0) {
        const landmarks = hands[0].keypoints;
        drawLandmarks(landmarks);
        const gesture = classifyGesture(landmarks);
        if (gesture && gestureMap[gesture]) {
            gestureText.innerText = gestureMap[gesture];
            speakGesture(gestureMap[gesture]);
        }
    }
    requestAnimationFrame(detectLoop);
}

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    return new Promise(resolve => {
        video.onloadedmetadata = () => {
            resolve(video);
        };
    });
}

async function main() {
    await setupCamera();
    video.play();
    await loadModel();
    detectLoop();
}

main();
