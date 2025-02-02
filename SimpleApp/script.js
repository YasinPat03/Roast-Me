const video = document.getElementById("camera");
const modeSwitch = document.getElementById("modeSwitch");
const modeTitle = document.getElementById("modeTitle");
const actionBtn = document.getElementById("actionBtn");
const responseText = document.getElementById("responseText");
const voiceToggle = document.getElementById("voiceToggle");

let isRoastMode = true;
let isVoiceEnabled = true; // Default: Voice enabled

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

    // Call AI Voice Function only if voice is enabled
    if (isVoiceEnabled) {
        speakText(response, type);
    }
}

// Function to use Google TTS API (Built-in Web Speech API)
function speakText(text, type) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    // Select different voices based on mode
    const voices = synth.getVoices();
    utterance.voice = voices.find(voice => 
        type === "roast" ? voice.name.includes("Daniel") : voice.name.includes("Samantha")
    ) || voices[0];

    utterance.rate = 1; // Speed
    utterance.pitch = type === "roast" ? 0.8 : 1.2; // Lower pitch for roasts, higher for compliments
    utterance.volume = 1;

    synth.speak(utterance);
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
}

// Toggle Voice Feature
function toggleVoice() {
    isVoiceEnabled = !isVoiceEnabled;
    voiceToggle.textContent = isVoiceEnabled ? "🔊 Voice On" : "🔇 Voice Off";
}

// Event Listeners
modeSwitch.addEventListener("click", toggleMode);
actionBtn.addEventListener("click", () => generateResponse(isRoastMode ? "roast" : "compliment"));
voiceToggle.addEventListener("click", toggleVoice);

// Ensure voices are loaded properly
window.speechSynthesis.onvoiceschanged = () => {
    console.log("Voices loaded:", window.speechSynthesis.getVoices());
};
