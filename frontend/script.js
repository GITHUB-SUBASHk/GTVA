const video = document.getElementById("webcam");
const gestureText = document.getElementById("gesture");
const statusDiv = document.getElementById("status");
let currentAudio = null;
let lastGesture = "";
let cooldown = false;

const gestureMap = {
  'Open_Palm': 'Hello',
  'Fist': 'Stop',
  'Thumbs_Up': 'Good job',
  'Peace': 'Peace',
  'OK': 'Okay'
};

async function setupCamera() {
    video.width = 640;
    video.height = 480;
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        return new Promise(resolve => {
            video.onloadedmetadata = () => {
                resolve(video);
            };
        });
    } catch (err) {
        statusDiv.textContent = "Camera access denied or unavailable.";
    }
}

function getApiUrl(path) {
    // Use relative path for API endpoint
    return `${window.location.origin}${path}`;
}

async function runDetection() {
    try {
        await setupCamera();
        video.play();
    } catch {
        return;
    }

    const gestureList = ["Thumbs Up", "Peace", "Open Palm", "Fist", "OK Sign"];
    setInterval(async () => {
        const gesture = gestureList[Math.floor(Math.random() * gestureList.length)];
        gestureText.innerText = gesture;
        statusDiv.textContent = `Sending gesture: ${gesture}`;
        try {
            const response = await fetch(getApiUrl("/speak"), {
                method: "POST",
                
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ gesture })
            });
            const data = await response.json();
            if (data.audio_url) {
                // Stop previous audio if playing
                if (currentAudio) {
                    currentAudio.pause();
                    currentAudio.currentTime = 0;
                }
                currentAudio = new Audio(getApiUrl(data.audio_url));
                currentAudio.play();
                statusDiv.textContent = `Playing audio for: ${gesture}`;
            } else if (data.error) {
                statusDiv.textContent = `Error: ${data.error}`;
            }
        } catch (err) {
            statusDiv.textContent = "Network or server error.";
        }
    }, 8000); // Detect every 8 seconds
}

async function loadModel() {
  return handpose.load();
}

function drawLandmarks(predictions) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  predictions.forEach(prediction => {
    prediction.landmarks.forEach(point => {
      ctx.beginPath();
      ctx.arc(point[0], point[1], 5, 0, 2 * Math.PI);
      ctx.fillStyle = "aqua";
      ctx.fill();
    });
  });
}

function classifyGesture(prediction) {
  if (!prediction || !prediction.landmarks) return null;
  // ...your gesture logic...
  return 'Open_Palm'; // Example, replace with real logic
}

function updateStatus(text) {
  document.getElementById('status').textContent = text;
}

function updateGesture(text) {
  document.getElementById('gesture').textContent = text;
}

function speak(text) {
  if (cooldown || text === lastGesture) return;
  lastGesture = text;
  cooldown = true;
  updateStatus(`Sending gesture: ${text}`);
  fetch('/speak', {
    method: 'POST',
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
        updateStatus(`Playing audio for: ${text}`);
      } else if (data.error) {
        updateStatus(`Error: ${data.error}`);
      }
      setTimeout(() => { cooldown = false; }, 4000);
    })
    .catch(() => updateStatus("Network or server error."));
}

async function detectHands() {
  const predictions = await model.estimateHands(video, true);
  drawLandmarks(predictions);
  if (predictions.length > 0) {
    const gesture = classifyGesture(predictions[0]);
    if (gesture && gestureMap[gesture]) {
      updateGesture(gestureMap[gesture]);
      speak(gestureMap[gesture]);
    }
  }
}

async function main() {
  await setupCamera();
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  model = await loadModel();
  setInterval(detectHands, 1000);
}

runDetection();
main();
