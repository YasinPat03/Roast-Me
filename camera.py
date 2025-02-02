from imutils import face_utils
import cv2
import dlib

# State Variables
xray_b = False
indices_b = False

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray, 0)

    for face in faces:

        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Assuming `shape` is a list of (x, y) tuples representing facial landmarks
        for i, (x, y) in enumerate(shape):
            print(f"Index {i}: ({x}, {y})")  # Prints the index and corresponding (x, y) coordinate

            if indices_b:
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)
            if xray_b:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)  



    # Display the output
    cv2.imshow("Face Landmarks", frame)


    key = cv2.waitKey(1) & 0xFF  # Capture the key only once per frame

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
