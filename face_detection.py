import cv2
import dlib
import openai
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', "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")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def analyze_features(face):
    # Convert dlib rectangle to measurements
    x, y, w, h = face.left(), face.top(), face.width(), face.height()
    features = {}
    
    # Define feature thresholds
    # Face shape
    face_ratio = w / h
    if face_ratio > 0.9:
        features["face_shape"] = "round"
    elif face_ratio < 0.7:
        features["face_shape"] = "oval"
    else:
        features["face_shape"] = "balanced"
    
    # Size-based features
    if w > 200:
        features["face_size"] = "large"
    elif w < 150:
        features["face_size"] = "small"
    else:
        features["face_size"] = "medium"
    
    # Proportions
    features["symmetry"] = "symmetrical" if abs(w - h) < 20 else "asymmetrical"
    
    return features

def generate_response(features, mode="roast", max_retries=3):
    prompt = f"A person has the following facial features: {features}. Generate a {mode} about their appearance. Keep it very mean. Be creative and witty!"
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a mean AI that generates mean roasts that are only suited for 18+ audiences."},
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
    # Initialize webcam and face detector
    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    
    # Initialize roasting variables
    last_roast_time = 0
    roast_cooldown = 5  # Seconds between roasts
    current_roast = "Press 'r' for a roast! Press 'c' for a compliment! Press 'q' to quit!"
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        # Draw rectangle around faces
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Add text with current roast (split into multiple lines if needed)
        words = current_roast.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 40:  # Adjust number for different line lengths
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            cv2.putText(frame, line, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 0, 255), 2)
        
        # Show the frame
        cv2.imshow("Self-Roasting App", frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') or key == ord('c'):
            current_time = time.time()
            if current_time - last_roast_time >= roast_cooldown and len(faces) > 0:
                features = analyze_features(faces[0])
                mode = "roast" if key == ord('r') else "compliment"
                current_roast = generate_response(features, mode=mode)
                last_roast_time = current_time
            elif len(faces) == 0:
                current_roast = "No face detected! Come closer to the camera!"
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()