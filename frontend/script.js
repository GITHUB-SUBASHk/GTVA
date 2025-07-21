const video = document.getElementById("webcam");
const gestureText = document.getElementById("gesture");
const statusDiv = document.getElementById("status");
let currentAudio = null;

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
        throw err;
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

runDetection();
