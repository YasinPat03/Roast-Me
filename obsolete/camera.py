# Dependancies
from imutils import face_utils
import cv2
import dlib
import openai

# Project Files
from face_measurements import FaceMeasurements
from face_analyzer import FaceAnalyzer

# Init
face_analyzer = FaceAnalyzer()
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# State Variables
xray_b = False
indices_b = False

# Fields
# At the top with your other imports and state variables
current_message = "Press 'r' for a roast! Press 'c' for a compliment! Press 'q' to quit!"
last_request_time = 0
cooldown = 5  # 5 second cooldown between requests


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray, 0)

    for face in faces:

        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Assuming `shape` is a list of (x, y) tuples representing facial landmarks
        for i, (x, y) in enumerate(shape):

            if indices_b:
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
            if xray_b:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  
        
        measurements = FaceMeasurements(shape)
        results = measurements.print_measurements()



    # Display the output
    cv2.imshow("Face Landmarks", frame)


    key = cv2.waitKey(1) & 0xFF  # Capture the key only once per frame

    features = face_analyzer.analyze_face(measurements)
    if key == ord('r'):  # roast mode
        prompts = face_analyzer.generate_prompt(features, mode="roast")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompts["system_prompt"]},
                {"role": "user", "content": prompts["user_prompt"]}
            ]
        )
        roast_text = response.choices[0].message.content.strip()

    # X-ray Mode Toggle
    if key == ord('x'):
        xray_b = not xray_b  # Toggle between True and False

    # Indices Toggle
    if key == ord('z'):
        indices_b = not indices_b  # Toggle between True and False

    # Quit the program
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
