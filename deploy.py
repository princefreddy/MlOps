import joblib
import numpy as np
import pandas as pd

class HousePriceCategorizer:
    def __init__(self, model_path='mlp_classifier_model.pkl'):
        """Initialize model with preprocessing objects"""
        saved_objects = joblib.load(model_path)
        self.model = saved_objects['model']
        self.scaler = saved_objects['scaler']
        self.label_encoder = saved_objects['label_encoder']
    
    def preprocess(self, input_data):
        """Preprocess input data"""
        # Ensure input is a DataFrame or convert it
        if not isinstance(input_data, pd.DataFrame):
            input_data = pd.DataFrame([input_data])
        
        # Scale features
        input_scaled = self.scaler.transform(input_data)
        return input_scaled
    
    def predict(self, input_data):
        """Predict house price category"""
        # Preprocess input
        input_scaled = self.preprocess(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_scaled)
        
        # Decode prediction
        return self.label_encoder.inverse_transform(prediction)[0]
    
    def predict_proba(self, input_data):
        """Get prediction probabilities"""
        # Preprocess input
        input_scaled = self.preprocess(input_data)
        
        # Get probabilities
        probas = self.model.predict_proba(input_scaled)
        
        # Create DataFrame with probabilities
        proba_df = pd.DataFrame(
            probas, 
            columns=self.label_encoder.classes_
        )
        
        return proba_df

def deploy_model():
    """Deploy model as a service/prediction interface"""
    categorizer = HousePriceCategorizer()
    
    # Example usage
    sample_data = {
        'feature_0': [10], 
        'feature_1': [20], 
        # Add other features as needed
    }
    
    print("Sample Prediction:")
    prediction = categorizer.predict(sample_data)
    print(f"Price Category: {prediction}")
    
    print("\nPrediction Probabilities:")
    probas = categorizer.predict_proba(sample_data)
    print(probas)

if __name__ == "__main__":
    deploy_model()
