const video = document.getElementById("camera");
const modeSwitch = document.getElementById("modeSwitch");
const modeTitle = document.getElementById("modeTitle");
const actionBtn = document.getElementById("actionBtn");
const responseText = document.getElementById("responseText");
const cameraError = document.getElementById("cameraError");

const roastSound = new Audio("audio.wav");
const complimentSound = new Audio("audio.wav");

let isRoastMode = true;

// Access the user's camera and display video feed
navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "user" } })
    .then((stream) => {
        video.srcObject = stream;
        cameraError.style.display = "none"; // Hide error if successful
    })
    .catch((err) => {
        console.error("Error accessing the camera: ", err);
        cameraError.style.display = "block"; // Show error message
    });

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

    if (type === "roast") roastSound.play();
    else complimentSound.play();
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

// Event Listeners
modeSwitch.addEventListener("click", toggleMode);
actionBtn.addEventListener("click", () => generateResponse(isRoastMode ? "roast" : "compliment"));
