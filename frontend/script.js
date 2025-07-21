const video = document.getElementById("video");
const gestureText = document.getElementById("gesture");
const statusDiv = document.getElementById("status");
let currentAudio = null;
let cooldown = false;

const gestureList = ["Open_Palm", "Fist", "Thumbs_Up", "Peace", "OK"];
const gestureMap = {
    "Open_Palm": "Hello",
    "Fist": "Stop",
    "Thumbs_Up": "Good job",
    "Peace": "Peace",
    "OK": "Okay"
};

async function setupCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    return new Promise(resolve => {
        video.onloadedmetadata = () => resolve(video);
    });
}

function speak(text) {
    if (cooldown) return;
    cooldown = true;
    fetch("/speak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gesture: text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.audio_url) {
            if (currentAudio) {
                currentAudio.pause();
                currentAudio.currentTime = 0;
            }
            currentAudio = new Audio(data.audio_url);
            currentAudio.play();
            statusDiv.textContent = `Playing audio for: ${text}`;
        }
        setTimeout(() => { cooldown = false; }, 4000);
    })
    .catch(() => {
        statusDiv.textContent = "Error communicating with backend.";
    });
}

async function main() {
    await setupCamera();
    video.play();

    setInterval(() => {
        const gesture = gestureList[Math.floor(Math.random() * gestureList.length)];
        gestureText.textContent = gestureMap[gesture];
        speak(gestureMap[gesture]);
    }, 8000);
}

main();
