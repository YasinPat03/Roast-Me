# Dependencies
from imutils import face_utils
import cv2
import dlib
from openai import OpenAI
import time

# Project Files
from face_measurements import FaceMeasurements # Make sure class name matches
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

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Landmark visualization
        for i, (x, y) in enumerate(shape):
            if indices_b:
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
            if xray_b:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  

        measurements = FaceMeasurements(shape)
        features = face_analyzer.analyze_face(measurements)

        # Handle roast/compliment requests
        current_time = time.time()
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
        # Display the current message
        words = current_message.split()
        y_position = 30
        line = []
        
        for word in words:
            line.append(word)
            if len(' '.join(line)) > 40:  # Line wrapping
                cv2.putText(frame, ' '.join(line), (10, y_position), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                y_position += 30
                line = []
                
        if line:  # Print any remaining words
            cv2.putText(frame, ' '.join(line), (10, y_position), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Face Landmarks", frame)

    # Key handling
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('x'):
        xray_b = not xray_b
    elif key == ord('z'):
        indices_b = not indices_b
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
