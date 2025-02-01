import cv2
import numpy as np
import openai
import time

OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load the pre-trained Haar Cascade model
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def detect_face(image_path):

    image = cv2.imread(image_path)
    if image is None:
        return None, 
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return None, 
    
    (x, y, w, h) = faces[0]
    return (x, y, w, h), None

def analyze_features(face, image_path):

    (x, y, w, h) = face
    features = {}
    
    # Define feature thresholds
    # Nose
    nose_width = w // 4
    if nose_width > 30:
        features["nose"] = "large"
    elif nose_width < 20:
        features["nose"] = "small"
    
    # Eyes
    eye_width = w // 3
    if eye_width > 40:
        features["eyes"] = "wide"
    elif eye_width < 30:
        features["eyes"] = "small"
    
    # Mouth
    mouth_width = w // 2
    if mouth_width > 50:
        features["mouth"] = "wide"
    elif mouth_width < 40:
        features["mouth"] = "small"
    
    # Eyebrows
    eyebrow_thickness = h // 10
    if eyebrow_thickness > 15:
        features["eyebrows"] = "thick"
    elif eyebrow_thickness < 10:
        features["eyebrows"] = "thin"
    
    # Jawline
    jawline_width = w // 2
    if jawline_width > 60:
        features["jawline"] = "strong"
    elif jawline_width < 50:
        features["jawline"] = "weak"
    
    # Cheekbones
    cheekbone_prominence = h // 5
    if cheekbone_prominence > 30:
        features["cheekbones"] = "high"
    elif cheekbone_prominence < 20:
        features["cheekbones"] = "flat"
    
    # Forehead
    forehead_height = h // 4
    if forehead_height > 40:
        features["forehead"] = "tall"
    elif forehead_height < 30:
        features["forehead"] = "short"
    
    # Face shape (round or oval)
    face_ratio = w / h
    if face_ratio > 0.9:
        features["face_shape"] = "round"
    elif face_ratio < 0.7:
        features["face_shape"] = "oval"
    
    # Chin
    chin_width = w // 5
    if chin_width < 20:
        features["chin"] = "pointy"
    elif chin_width > 30:
        features["chin"] = "wide"
    
    return features

def generate_response(features, mode="roast", max_retries=3):

    prompt = f"A person has the following facial features: {features}. Generate a {mode} about their appearance. Be creative, witty, and engaging."
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=[
                    {"role": "system", "content": "You are a humorous AI that generates funny and lighthearted roasts and sincere compliments."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except openai.RateLimitError:
            wait_time = (2 ** attempt) + 1  
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return "Error generating response."
    return "Failed to generate response after multiple attempts."

if __name__ == "__main__":
    image_path = "tested.jpg" 
    face, error = detect_face(image_path)
    
    if error:
        print(error)
    else:
        features = analyze_features(face, image_path)
        print("Detected features:", features)
        
        roast = generate_response(features, mode="roast")
        print("Roast:", roast)
        
        compliment = generate_response(features, mode="compliment")
        print("Compliment:", compliment)