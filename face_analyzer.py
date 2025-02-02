class FaceAnalyzer:
    def __init__(self):
        """
        Initialize with expanded thresholds for facial features and emotions
        """
        # Distance-based personality indicators (in cm)
        self.distance_thresholds = {
            'very_close': 30,    # Less than 30cm: very confident/intimate
            'close': 45,         # 30-45cm: confident
            'medium': 60,        # 45-60cm: neutral
            'far': 80,          # 60-80cm: slightly reserved
            'very_far': float('inf')  # >80cm: shy/reserved
        }

        self.thresholds = {
            # Basic Features
            'nose_width': {
                'tiny': 0.12,
                'small': 0.15,
                'medium': 0.22,
                'large': 0.28,
                'very_large': float('inf')
            },
            'eye_ratio': {  # width/height ratio
                'very_round': 1.8,
                'round': 2.0,
                'normal': 2.5,
                'almond': 3.0,
                'narrow': float('inf')
            },
            'face_width': {
                'very_narrow': 0.7,
                'narrow': 0.8,
                'medium': 0.95,
                'wide': 1.1,
                'very_wide': float('inf')
            },
            'mouth_gap': {
                'sealed': 0.01,
                'closed': 0.02,
                'relaxed': 0.05,
                'open': 0.1,
                'wide_open': float('inf')
            },
            # Advanced Features
            'eye_spacing': {
                'close_set': 0.25,
                'normal': 0.35,
                'wide_set': float('inf')
            },
            'lip_fullness': {  # height to width ratio
                'thin': 0.15,
                'medium': 0.25,
                'full': 0.35,
                'very_full': float('inf')
            },
            'nose_prominence': {  # nose height relative to face
                'low': 0.3,
                'medium': 0.4,
                'high': float('inf')
            }
        }

        # Emotional State Combinations
        self.emotion_patterns = {
            'happy': {
                'mouth_gap': ['relaxed', 'open'],
                'lip_width': 0.5,  # threshold for smile detection
            },
            'sad': {
                'mouth_gap': ['sealed', 'closed'],
                'lip_width': 0.3,  # threshold for frown detection
            },
            'surprised': {
                'mouth_gap': ['open', 'wide_open'],
                'eye_height': 0.4,  # threshold for wide eyes
            },
            'neutral': {
                'mouth_gap': ['relaxed'],
                'lip_width': 0.4,  # neutral lip width
            }
        }

    def analyze_face(self, measurements):
        """
        Enhanced analysis of facial measurements returning detailed features, emotions,
        and distance-based personality traits
        """
        features = {}
        
        # Basic Feature Analysis
        features['nose'] = self._analyze_threshold('nose_width', measurements.nose_width)
        features['face_shape'] = self._analyze_threshold('face_width', measurements.facial_width)
        features['mouth_state'] = self._analyze_threshold('mouth_gap', measurements.mouth_gap)
        
        # Eye Analysis
        left_eye_ratio = measurements.eye_width_l / measurements.eye_height_l
        right_eye_ratio = measurements.eye_width_r / measurements.eye_height_r
        avg_eye_ratio = (left_eye_ratio + right_eye_ratio) / 2
        features['eye_shape'] = self._analyze_threshold('eye_ratio', avg_eye_ratio)
        features['eye_spacing'] = self._analyze_threshold('eye_spacing', measurements.eye_distance)
        
        # Advanced Feature Analysis
        features['lip_fullness'] = self._analyze_threshold('lip_fullness', measurements.lip_height / measurements.lip_width)
        features['nose_prominence'] = self._analyze_threshold('nose_prominence', measurements.nose_height)
        
        # Symmetry Analysis
        asymmetry_scores = {
            'eye_width': abs(measurements.eye_width_l - measurements.eye_width_r),
            'eye_height': abs(measurements.eye_height_l - measurements.eye_height_r)
        }
        features['symmetry'] = self._analyze_asymmetry(asymmetry_scores)
        
        # Emotional State Analysis
        features['emotion'] = self._analyze_emotion(measurements)
        
        # Personality Traits (based on facial features)
        features['personality_indicators'] = self._analyze_personality(features)
        
        # Distance-based personality analysis
        features['distance_personality'] = self._analyze_distance_personality(measurements.distance)
        
        return features

    def _analyze_threshold(self, feature, value):
        """Helper method to analyze a value against thresholds"""
        for category, threshold in self.thresholds[feature].items():
            if value < threshold:
                return category
        return list(self.thresholds[feature].keys())[-1]

    def _analyze_asymmetry(self, scores):
        """Analyze multiple asymmetry scores to determine overall symmetry"""
        total_asymmetry = sum(scores.values())
        if total_asymmetry < 0.05:
            return "highly_symmetrical"
        elif total_asymmetry < 0.1:
            return "symmetrical"
        elif total_asymmetry < 0.15:
            return "slightly_asymmetrical"
        else:
            return "asymmetrical"

    def _analyze_emotion(self, measurements):
        """
        Analyze emotional state based on available measurements
        Returns primary emotion and confidence score
        """
        emotion_scores = {}
        
        # Check each emotion pattern
        for emotion, pattern in self.emotion_patterns.items():
            score = 0
            total_checks = len(pattern)
            
            # Check mouth gap
            if 'mouth_gap' in pattern:
                mouth_state = self._analyze_threshold('mouth_gap', measurements.mouth_gap)
                if mouth_state in pattern['mouth_gap']:
                    score += 1
            
            # Check lip width (for smile/frown detection)
            if 'lip_width' in pattern:
                if measurements.lip_width >= pattern['lip_width']:
                    score += 1
            
            # Check eye height (for surprise detection)
            if 'eye_height' in pattern:
                avg_eye_height = (measurements.eye_height_l + measurements.eye_height_r) / 2
                if avg_eye_height >= pattern['eye_height']:
                    score += 1
            
            emotion_scores[emotion] = score / total_checks

        # Get the highest scoring emotion
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return {
            'primary': primary_emotion[0],
            'confidence': primary_emotion[1]
        }

    def _analyze_distance_personality(self, distance):
        """
        Analyze personality traits based on camera distance
        Returns both the distance category and associated personality traits
        """
        # Determine distance category
        category = "very_far"
        for dist_category, threshold in self.distance_thresholds.items():
            if distance < threshold:
                category = dist_category
                break
        
        # Associate personality traits with distance
        personality_traits = {
            'very_close': ['outgoing', 'confident', 'dominant'],
            'close': ['friendly', 'engaging', 'assertive'],
            'medium': ['balanced', 'comfortable', 'neutral'],
            'far': ['reserved', 'thoughtful', 'careful'],
            'very_far': ['shy', 'introverted', 'observant']
        }
        
        return {
            'category': category,
            'distance_cm': distance,
            'traits': personality_traits[category]
        }

    def _analyze_personality(self, features):
        """
        Infer potential personality traits based on facial features
        This is based on physiognomy theories (for entertainment purposes)
        """
        traits = []
        
        if features['eye_shape'] in ['round', 'very_round']:
            traits.append('expressive')
        elif features['eye_shape'] in ['narrow', 'almond']:
            traits.append('analytical')
            
        if features['face_shape'] in ['wide', 'very_wide']:
            traits.append('outgoing')
        elif features['face_shape'] in ['narrow', 'very_narrow']:
            traits.append('reserved')
            
        if features['lip_fullness'] in ['full', 'very_full']:
            traits.append('passionate')
        elif features['lip_fullness'] == 'thin':
            traits.append('disciplined')
            
        return traits

    def generate_prompt(self, features, mode="roast"):
        """
        Enhanced prompt generation including emotional state and personality traits
        """
        if mode == "roast":
            system_prompt = """You are a witty roast generator that creates clever, funny roasts based on facial features and emotional state. 
            Keep roasts playful and avoid crossing the line into cruel or offensive territory. 
            Focus on being clever rather than mean-spirited. Maximum 2 sentences."""
            
            user_prompt = f"""Generate a playful roast for someone with these characteristics:
            - Face shape: {features['face_shape']}
            - Eyes: {features['eye_shape']} and {features['eye_spacing']}
            - Nose: {features['nose']}
            - Mouth: {features['mouth_state']}
            - Symmetry: {features['symmetry']}
            - Current emotion: {features['emotion']['primary']} (confidence: {features['emotion']['confidence']:.2f})
            - Distance: {features['distance_personality']['category']} ({features['distance_personality']['distance_cm']:.1f}cm)
            - Personality indicators: {', '.join(features['personality_indicators'])}
            - Distance-based traits: {', '.join(features['distance_personality']['traits'])}"""

        else:  # compliment mode
            system_prompt = """You are a genuine compliment generator that creates kind, specific compliments based on facial features and emotional state.
            Focus on positive aspects and unique characteristics. Maximum 2 sentences."""
            
            user_prompt = f"""Generate a genuine compliment for someone with these characteristics:
            - Face shape: {features['face_shape']}
            - Eyes: {features['eye_shape']} and {features['eye_spacing']}
            - Nose: {features['nose']}
            - Mouth: {features['mouth_state']}
            - Symmetry: {features['symmetry']}
            - Current emotion: {features['emotion']['primary']} (confidence: {features['emotion']['confidence']:.2f})
            - Personality indicators: {', '.join(features['personality_indicators'])}"""

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }