from transformers import pipeline
from PIL import Image

# --- Zero-Shot Text Classification Class ---
class TextClassifierModel:
    """
    Manages the Zero-Shot Text Classification model.
    Loads the model once and provides a clean interface to classify text.
    """
    def __init__(self, model_name="facebook/bart-large-mnli"):
        # The model is loaded here when your teammate runs the app for the first time
        print(f"Loading Text Classifier: {model_name}...")
        self.classifier = pipeline(
            "zero-shot-classification", 
            model=model_name
        )
        print("Text Classifier loaded successfully.")

    def classify(self, text, labels):
        """
        Input: text (str), labels (list of str)
        Output: dict {'label': str, 'score': float} or {'error': str}
        """
        if not text or not labels:
            return {'error': "Text or candidate labels cannot be empty."}
            
        result = self.classifier(text, labels)
        
        # Returns the top result formatted for easy GUI use
        return {
            'label': result['labels'][0],
            'score': round(result['scores'][0] * 100, 2)
        }

# --- Image Classification Class ---
class ImageClassifierModel:
    """
    Manages the Image Classification model.
    Initializes the pipeline once and provides a clean interface to classify an image from a file path.
    """
    def __init__(self, model_name="google/vit-base-patch16-224"):
        # The model is loaded here when your teammate runs the app for the first time
        print(f"Loading Image Classifier: {model_name}...")
        self.classifier = pipeline(
            "image-classification", 
            model=model_name
        )
        print("Image Classifier loaded successfully.")
    
    def classify(self, image_path):
        """
        Input: image_path (str)
        Output: dict {'label': str, 'score': float} or {'error': str}
        """
        try:
            # 1. Open the image using Pillow (PIL)
            image = Image.open(image_path)
            
            # 2. Run the classification
            result = self.classifier(image)
            
            # Returns the top result formatted for easy GUI use
            return {
                'label': result[0]['label'],
                'score': round(result[0]['score'] * 100, 2)
            }

        except FileNotFoundError:
            return {'error': "Image file not found at the specified path."}
        except Exception as e:
            return {'error': f"An error occurred during classification: {e}"}