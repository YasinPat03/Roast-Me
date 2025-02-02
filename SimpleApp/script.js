const video = document.getElementById("camera");
const modeSwitch = document.getElementById("modeSwitch");
const modeTitle = document.getElementById("modeTitle");
const actionBtn = document.getElementById("actionBtn");
const responseText = document.getElementById("responseText");
const voiceToggle = document.getElementById("voiceToggle");

let isRoastMode = true;
let isVoiceEnabled = true;
let currentAudio = null;
let stream = null;

// ElevenLabs API Key
const API_KEY = "sk_0301a5e5ab5c39edfe24616ecda9ba2e7a9f11af617ebf5d";

// ElevenLabs Voice IDs
const ROAST_VOICE_ID = "pNInz6obpgDQGcFmaJgB"; // Deep male voice for roasts
const COMPLIMENT_VOICE_ID = "ErXwobaYiN019PkySvjV"; // Soft female voice for compliments

// Initialize camera
async function initCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing camera:", err);
        responseText.textContent = "Error accessing camera. Please make sure you've granted camera permissions.";
    }
}

// Function to capture frame and send to server
async function captureAndAnalyze() {
    try {
        // Create a canvas to capture the current frame
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
        
        // Convert to base64
        const imageData = canvas.toDataURL('image/jpeg');
        
        // Show loading state
        responseText.textContent = "Analyzing...";
        actionBtn.disabled = true;
        
        // Send to server
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData,
                mode: isRoastMode ? 'roast' : 'compliment'
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Display response
        responseText.textContent = data.response;
        
        // Generate voice if enabled
        if (isVoiceEnabled) {
            generateAIVoice(data.response, isRoastMode ? 'roast' : 'compliment');
        }
    } catch (error) {
        responseText.textContent = `Error: ${error.message}`;
    } finally {
        actionBtn.disabled = false;
    }
}

// Function to generate AI voice from ElevenLabs
async function generateAIVoice(text, type) {
    const voiceId = type === "roast" ? ROAST_VOICE_ID : COMPLIMENT_VOICE_ID;
    
    try {
        const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "xi-api-key": API_KEY
            },
            body: JSON.stringify({
                text: text,
                model_id: "eleven_monolingual_v1",
                voice_settings: {
                    stability: 0.5,
                    similarity_boost: 0.8
                }
            })
        });

        if (!response.ok) {
            throw new Error("Failed to generate TTS");
        }

        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        playAudio(audioUrl);
    } catch (error) {
        console.error("Error with AI voice request:", error);
    }
}

// Function to play AI-generated audio
function playAudio(audioUrl) {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    currentAudio = new Audio(audioUrl);
    currentAudio.play();
}

// Toggle Roast/Compliment Mode
function toggleMode() {
    isRoastMode = !isRoastMode;

    if (isRoastMode) {
        document.body.classList.remove("compliment-mode");
        modeSwitch.textContent = "💚";
        modeTitle.textContent = "🔥 Roast Mode 🔥";
        actionBtn.textContent = "Roast Me";
    } else {
        document.body.classList.add("compliment-mode");
        modeSwitch.textContent = "🔥";
        modeTitle.textContent = "💚 Compliment Mode 💚";
        actionBtn.textContent = "Compliment Me";
    }

    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
}

// Toggle Voice Feature
function toggleVoice() {
    isVoiceEnabled = !isVoiceEnabled;
    voiceToggle.textContent = isVoiceEnabled ? "🔊 Voice On" : "🔇 Voice Off";

    if (!isVoiceEnabled && currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
}

// Event Listeners
modeSwitch.addEventListener("click", toggleMode);
actionBtn.addEventListener("click", captureAndAnalyze);
voiceToggle.addEventListener("click", toggleVoice);

// Initialize camera on load
initCamera();