// static/js/script.js
const video = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const predictionElement = document.getElementById('prediction');

async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam:", err);
        predictionElement.textContent = "Webcam error";
    }
}

function sendFrameToBackend() {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg', 0.5);
    
    const ws = new WebSocket('ws://' + window.location.host + '/ws');
    
    ws.onopen = () => {
        ws.send(dataURL);
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        predictionElement.textContent = data.gesture;
        ws.close(); // Close after receiving prediction to avoid multiple connections
    };
    
    ws.onclose = () => {
        setTimeout(sendFrameToBackend, 100); // Reconnect for next frame
    };
    
    ws.onerror = (err) => {
        console.error("WebSocket error:", err);
        predictionElement.textContent = "Connection error";
    };
}

video.addEventListener('play', () => {
    setInterval(sendFrameToBackend, 200); // Send frame every 200ms
});

startWebcam();