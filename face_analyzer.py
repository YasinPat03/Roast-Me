class FaceAnalyzer:
    def __init__(self):
        """
        Initialize with default thresholds for facial features
        """
        # Thresholds for various facial features
        self.thresholds = {
            'nose_width': {
                'small': 0.15,
                'medium': 0.22,
                'large': float('inf')
            },
            'eye_ratio': {  # width/height ratio
                'round': 2.0,
                'normal': 2.5,
                'narrow': float('inf')
            },
            'face_width': {
                'narrow': 0.8,
                'medium': 0.95,
                'wide': float('inf')
            },
            'mouth_gap': {
                'closed': 0.02,
                'normal': 0.05,
                'open': float('inf')
            }
        }

    def analyze_face(self, measurements):
        """
        Analyze facial measurements and return feature descriptions
        """
        features = {}
        
        # Analyze nose
        if measurements.nose_width < self.thresholds['nose_width']['small']:
            features['nose'] = "tiny"
        elif measurements.nose_width < self.thresholds['nose_width']['medium']:
            features['nose'] = "normal"
        else:
            features['nose'] = "large"

        # Analyze eyes
        left_eye_ratio = measurements.eye_width_l / measurements.eye_height_l
        right_eye_ratio = measurements.eye_width_r / measurements.eye_height_r
        avg_eye_ratio = (left_eye_ratio + right_eye_ratio) / 2
        
        if avg_eye_ratio < self.thresholds['eye_ratio']['round']:
            features['eyes'] = "round"
        elif avg_eye_ratio < self.thresholds['eye_ratio']['normal']:
            features['eyes'] = "normal"
        else:
            features['eyes'] = "narrow"

        # Analyze face width
        if measurements.facial_width < self.thresholds['face_width']['narrow']:
            features['face_shape'] = "narrow"
        elif measurements.facial_width < self.thresholds['face_width']['medium']:
            features['face_shape'] = "balanced"
        else:
            features['face_shape'] = "wide"

        # Analyze mouth state
        if measurements.mouth_gap < self.thresholds['mouth_gap']['closed']:
            features['mouth'] = "closed"
        elif measurements.mouth_gap < self.thresholds['mouth_gap']['normal']:
            features['mouth'] = "normal"
        else:
            features['mouth'] = "open"

        # Add asymmetry analysis
        eye_asymmetry = abs(measurements.eye_width_l - measurements.eye_width_r)
        if eye_asymmetry > 0.1:  # threshold for noticeable asymmetry
            features['symmetry'] = "asymmetrical"
        else:
            features['symmetry'] = "symmetrical"

        return features

    def generate_prompt(self, features, mode="roast"):
        """
        Generate an AI prompt based on facial features
        """
        if mode == "roast":
            system_prompt = """You are a witty roast generator that creates clever, funny roasts based on facial features. 
            Keep roasts playful and avoid crossing the line into cruel or offensive territory. 
            Focus on being clever rather than mean-spirited. Maximum 2 sentences."""
            
            user_prompt = f"""Generate a playful roast for someone with these facial features:
            - Face shape: {features['face_shape']}
            - Eyes: {features['eyes']}
            - Nose: {features['nose']}
            - Mouth: {features['mouth']}
            - Symmetry: {features['symmetry']}"""

        else:  # compliment mode
            system_prompt = """You are a genuine compliment generator that creates kind, specific compliments based on facial features.
            Focus on positive aspects and unique characteristics. Maximum 2 sentences."""
            
            user_prompt = f"""Generate a genuine compliment for someone with these facial features:
            - Face shape: {features['face_shape']}
            - Eyes: {features['eyes']}
            - Nose: {features['nose']}
            - Mouth: {features['mouth']}
            - Symmetry: {features['symmetry']}"""

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }