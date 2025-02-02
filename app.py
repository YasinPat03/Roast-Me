from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import cv2
import numpy as np
import dlib
from imutils import face_utils
from openai import OpenAI
import io
import os

from face_measurements import FaceMeasurements
from face_analyzer import FaceAnalyzer
from config import OPENAI_API_KEY

app = Flask(__name__, static_folder='SimpleApp')
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize face detection/analysis tools
face_analyzer = FaceAnalyzer()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Serve static files from SimpleApp directory
@app.route('/')
def index():
    return send_from_directory('SimpleApp', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('SimpleApp', path)

@app.route('/analyze', methods=['POST'])
def analyze_face():
    try:
        # Get the base64 image from the request
        data = request.json
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64,
        image_bytes = base64.b64decode(image_data)
        
        # Convert to opencv format
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = detector(gray, 0)
        
        if len(faces) == 0:
            return jsonify({'error': 'No face detected'}), 400
            
        # Get the first face
        face = faces[0]
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)
        
        # Get measurements and analysis
        measurements = FaceMeasurements(shape)
        features = face_analyzer.analyze_face(measurements)
        
        # Generate prompt based on mode
        mode = data.get('mode', 'roast')
        prompts = face_analyzer.generate_prompt(features, mode=mode)
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompts["system_prompt"]},
                {"role": "user", "content": prompts["user_prompt"]}
            ]
        )
        
        result = response.choices[0].message.content.strip()
        return jsonify({'response': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)