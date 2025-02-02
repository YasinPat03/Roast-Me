# Dependencies
from imutils import face_utils
import cv2
import dlib
from openai import OpenAI
import time

# Project Files
from face_measurements import FaceMeasurements
from face_analyzer import FaceAnalyzer
from config import OPENAI_API_KEY

# OpenAI setup
client = OpenAI(api_key=OPENAI_API_KEY)

# Init
face_analyzer = FaceAnalyzer()
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# State Variables
xray_b = False
indices_b = False
current_message = "Press 'r' for a roast! Press 'c' for a compliment! Press 'q' to quit!"
last_request_time = 0
cooldown = 5

def draw_text_multiline(frame, text, start_pos=(10, 30), font_scale=0.7, color=(0, 0, 255), thickness=2):
    """Helper function to draw multi-line text on frame"""
    words = text.split()
    x, y = start_pos
    line = []
    
    for word in words:
        line.append(word)
        text_size = cv2.getTextSize(' '.join(line), cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        
        if text_size[0] > frame.shape[1] - 20:  # 20px margin
            cv2.putText(frame, ' '.join(line[:-1]), (x, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
            y += 30
            line = [word]
    
    if line:
        cv2.putText(frame, ' '.join(line), (x, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    # Always display the current message
    draw_text_multiline(frame, current_message)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Draw face rectangle
        x, y = face.left(), face.top()
        w, h = face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Add "Say Cheese!" text below the rectangle
        cheese_text = "Say Cheese!"
        text_size = cv2.getTextSize(cheese_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = x + (w - text_size[0]) // 2  # Center text horizontally
        text_y = y + h + 20  # Place text 20 pixels below rectangle
        cv2.putText(frame, cheese_text, (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Landmarks visualization (debug features)
        for i, (x, y) in enumerate(shape):
            if indices_b:
                cv2.putText(frame, str(i), (x, y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
            if xray_b:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Process measurements
        measurements = FaceMeasurements(shape)
        features = face_analyzer.analyze_face(measurements)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    current_time = time.time()
    
    # Handle roast/compliment requests
    if key in [ord('r'), ord('c')] and current_time - last_request_time >= cooldown:
        mode = "roast" if key == ord('r') else "compliment"
        prompts = face_analyzer.generate_prompt(features, mode=mode)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompts["system_prompt"]},
                    {"role": "user", "content": prompts["user_prompt"]}
                ]
            )
            current_message = response.choices[0].message.content.strip()
            last_request_time = current_time
        except Exception as e:
            current_message = f"Error: {str(e)}"
    
    # Debug mode toggles (hidden but functional)
    elif key == ord('x'):
        xray_b = not xray_b
    elif key == ord('z'):
        indices_b = not indices_b
    elif key == ord('q'):
        break

    # Show frame
    cv2.imshow("Face Analyzer", frame)

cap.release()
cv2.destroyAllWindows()