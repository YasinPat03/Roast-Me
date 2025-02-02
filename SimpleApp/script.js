const video = document.getElementById("camera");
const modeSwitch = document.getElementById("modeSwitch");
const modeTitle = document.getElementById("modeTitle");
const actionBtn = document.getElementById("actionBtn");
const responseText = document.getElementById("responseText");
const voiceToggle = document.getElementById("voiceToggle");

let isRoastMode = true;
let isVoiceEnabled = true; // Default: Voice enabled

// ElevenLabs API Key (Use a backend proxy for security!)
const API_KEY = "sk_0301a5e5ab5c39edfe24616ecda9ba2e7a9f11af617ebf5d";

// ElevenLabs Voice IDs
const ROAST_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"; // Deep male voice for roasts
const COMPLIMENT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"; // Soft female voice for compliments

let currentAudio = null; // Track current audio to prevent duplicates

// Roasts & Compliments Data
const roasts = [
    "You bring everyone so much joy... when you leave the room!",
    "You're like a cloud. When you disappear, it's a beautiful day!",
    "You're proof that even AI can feel secondhand embarrassment.",
];

const compliments = [
    "You light up the room with your smile!",
    "You're more unique than a rare Pokémon!",
    "You're not just cool—you're next-level awesome!",
];

// Function to generate a roast or compliment
function generateResponse(type) {
    const list = type === "roast" ? roasts : compliments;
    const randomIndex = Math.floor(Math.random() * list.length);
    const response = list[randomIndex];

    responseText.textContent = response;

    // Stop any currently playing voice
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    // Call AI Voice Function only if voice is enabled
    if (isVoiceEnabled) {
        generateAIVoice(response, type);
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
        console.error("Error with AI voice request", error);
    }
}

// Function to play AI-generated audio (Ensuring only one plays at a time)
function playAudio(audioUrl) {
    if (currentAudio) {
        currentAudio.pause(); // Stop any ongoing audio
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
        actionBtn.onclick = () => generateResponse("roast");
    } else {
        document.body.classList.add("compliment-mode");
        modeSwitch.textContent = "🔥";
        modeTitle.textContent = "💚 Compliment Mode 💚";
        actionBtn.textContent = "Compliment Me";
        actionBtn.onclick = () => generateResponse("compliment");
    }

    // Stop any ongoing speech when switching modes
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
}

// Toggle Voice Feature
function toggleVoice() {
    isVoiceEnabled = !isVoiceEnabled;
    voiceToggle.textContent = isVoiceEnabled ? "🔊 Voice On" : "🔇 Voice Off";

    // Stop ongoing speech when turning voice off
    if (!isVoiceEnabled && currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }
}

// Event Listeners
modeSwitch.addEventListener("click", toggleMode);
actionBtn.addEventListener("click", () => generateResponse(isRoastMode ? "roast" : "compliment"));
voiceToggle.addEventListener("click", toggleVoice);
