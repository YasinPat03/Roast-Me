class FaceMeasurements:
    def __init__(self, shape, real_face_width=14.0, focal_length=550):  # 14cm average face width, 550px estimated focal length
        """
        Initialize facial measurements from landmarks, normalized by facial height
        Includes rough distance estimation for 720p webcam
        """
        # Calculate facial height and width
        self.facial_height = (shape[8][1] - shape[27][1]) * (3/2)
        self.pixel_face_width = abs(shape[1][0] - shape[15][0])
        
        # Rough distance estimation in cm
        self.distance = (real_face_width * focal_length) / self.pixel_face_width
        
        # Normalized width measurements (x-coordinates)
        self.facial_width = abs(shape[1][0] - shape[15][0]) / self.facial_height
        self.nose_width = abs(shape[31][0] - shape[35][0]) / self.facial_height
        self.lip_width = abs(shape[46][0] - shape[54][0]) / self.facial_height
        self.eye_distance = abs(shape[39][0] - shape[42][0]) / self.facial_height
        self.eye_width_l = abs(shape[36][0] - shape[39][0]) / self.facial_height
        self.eye_width_r = abs(shape[42][0] - shape[45][0]) / self.facial_height
        
        # Normalized height measurements (y-coordinates)
        self.nose_height = (shape[33][1] - shape[27][1]) / self.facial_height
        self.lip_height = (shape[57][1] - shape[66][1]) / self.facial_height
        self.mouth_gap = (shape[66][1] - shape[62][1]) / self.facial_height
        self.eye_height_l = (shape[40][1] - shape[38][1]) / self.facial_height
        self.eye_height_r = (shape[47][1] - shape[43][1]) / self.facial_height

    def print_measurements(self):
        """
        Prints all measurements in a formatted way
        """
        print("\nDistance Estimation:")
        print(f"Distance from camera: {self.distance:.1f} cm ({self.distance/100:.1f} meters)")
        
        print("\nFacial Measurements (normalized by facial height)")
        print("============================================")
        
        print("\nWidth Measurements:")
        print(f"Facial Width: {self.facial_width:.3f}")
        print(f"Nose Width: {self.nose_width:.3f}")
        print(f"Lip Width: {self.lip_width:.3f}")
        print(f"Eye Distance: {self.eye_distance:.3f}")
        print(f"Left Eye Width: {self.eye_width_l:.3f}")
        print(f"Right Eye Width: {self.eye_width_r:.3f}")
        
        print("\nHeight Measurements:")
        print(f"Nose Height: {self.nose_height:.3f}")
        print(f"Lip Height: {self.lip_height:.3f}")
        print(f"Mouth Gap: {self.mouth_gap:.3f}")
        print(f"Left Eye Height: {self.eye_height_l:.3f}")
        print(f"Right Eye Height: {self.eye_height_r:.3f}")

    def get_measurements(self):
        results = {
            'distance_cm': self.distance,
            'distance_m': self.distance/100,
            
            # Width measurements
            'facial_width': self.facial_width,
            'nose_width': self.nose_width,
            'lip_width': self.lip_width,
            'eye_distance': self.eye_distance,
            'eye_width_l': self.eye_width_l,
            'eye_width_r': self.eye_width_r,
            
            # Height measurements
            'nose_height': self.nose_height,
            'lip_height': self.lip_height,
            'mouth_gap': self.mouth_gap,
            'eye_height_l': self.eye_height_l,
            'eye_height_r': self.eye_height_r
        }
        return results