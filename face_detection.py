import cv2
import numpy as np
import openai
import time
import os
from dotenv import load_dotenv

# Load environment variables (create a .env file with your API key)
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "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")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Get OpenCV's Haar Cascade file path
opencv_path = os.path.dirname(cv2.__file__)
haar_cascade_path = os.path.join(opencv_path, 'data', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(haar_cascade_path)

def analyze_features(face):
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
    
    # Face shape
    face_ratio = w / h
    if face_ratio > 0.9:
        features["face_shape"] = "round"
    elif face_ratio < 0.7:
        features["face_shape"] = "oval"
    
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

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    last_roast_time = 0
    roast_cooldown = 5  # Seconds between roasts
    current_roast = "Press 'r' for a roast!"
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Draw rectangle around faces and display current roast
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Add text with current roast
        cv2.putText(frame, current_roast[:50], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if len(current_roast) > 50:
            cv2.putText(frame, current_roast[50:100], (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show the frame
        cv2.imshow('Roast Me App', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            current_time = time.time()
            if current_time - last_roast_time >= roast_cooldown and len(faces) > 0:
                features = analyze_features(faces[0])
                current_roast = generate_response(features, mode="roast")
                last_roast_time = current_time
            elif len(faces) == 0:
                current_roast = "No face detected! Are you camera shy?"
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()