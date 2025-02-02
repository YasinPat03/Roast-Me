from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import dlib
import numpy as np
import openai
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize face detector
detector = dlib.get_frontal_face_detector()

def analyze_features(face):
    x, y, w, h = face.left(), face.top(), face.width(), face.height()
    features = {}
    
    # Face shape analysis
    face_ratio = w / h
    if face_ratio > 0.9:
        features["face_shape"] = "round"
    elif face_ratio < 0.7:
        features["face_shape"] = "oval"
    else:
        features["face_shape"] = "balanced"
    
    # Size features
    if w > 200:
        features["face_size"] = "large"
    elif w < 150:
        features["face_size"] = "small"
    else:
        features["face_size"] = "medium"
    
    features["symmetry"] = "symmetrical" if abs(w - h) < 20 else "asymmetrical"
    
    return features

def generate_response(features, mode="roast"):
    prompt = f"A person has the following facial features: {features}. Generate a {mode} about their appearance. Keep it very mean. Be creative and witty!"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mean AI that generates mean roasts that are only suited for 18+ audiences."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Failed to generate response"

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # Read and process the image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return {"error": "Invalid image"}
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    if not faces:
        return {"error": "No face detected"}
    
    # Analyze the first detected face
    features = analyze_features(faces[0])
    roast = generate_response(features, "roast")
    
    # Draw rectangle around face
    face = faces[0]
    x, y, w, h = face.left(), face.top(), face.width(), face.height()
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Convert processed image to base64
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return {
        "features": features,
        "roast": roast,
        "image": img_base64
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)