import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI

app = FastAPI()

class HousePriceCategorizer:
    def __init__(self, model_path='mlp_classifier_model.pkl', preprocessing_path='preprocessing_objects.pkl'):
        """Initialize model"""
        # Load the trained model
        saved_objects = joblib.load(model_path)
        self.model = saved_objects['model']
        
        # Load preprocessing objects
        preprocessing_objects = joblib.load(preprocessing_path)
        self.preprocessor = preprocessing_objects['preprocessor']
        self.pca = preprocessing_objects['pca']
    
    def handle_missing_values(self, input_data):
        """Handle missing values in the input data"""
        # Remove columns with more than 50% missing values
        missing_percentage = input_data.isnull().mean() * 100
        columns_to_drop = missing_percentage[missing_percentage > 50].index.tolist()
        input_data_cleaned = input_data.drop(columns=columns_to_drop)
        
        # Fill remaining missing values with the most frequent value
        input_data_cleaned = input_data_cleaned.apply(lambda x: x.fillna(x.value_counts().index[0]))
        
        return input_data_cleaned
    
    def preprocess(self, input_data):
        """Preprocess input data"""
        # Handle missing values
        input_data_cleaned = self.handle_missing_values(input_data)
        
        # Ensure the column "FireplaceQu" is present
        if "FireplaceQu" not in input_data_cleaned.columns:
            input_data_cleaned["FireplaceQu"] = "TA"  # Default value
        
        # Apply preprocessing (One-Hot Encoding and Scaling)
        input_transformed = self.preprocessor.transform(input_data_cleaned)
        
        # Apply PCA
        input_pca = self.pca.transform(input_transformed)
        
        return input_pca
    
    def predict(self, input_data):
        """Predict house price category"""
        # Preprocess input
        input_pca = self.preprocess(input_data)
        
        # Make prediction
        prediction = self.model.predict(input_pca)
        
        return prediction[0]  # Return the first prediction

# Initialize the categorizer
categorizer = HousePriceCategorizer()

@app.get("/predict")
async def get_prediction():
    """Endpoint to get the prediction for the first row of test.csv"""
    # Load test data
    test_data = pd.read_csv('test.csv')
    
    # Make prediction
    prediction = categorizer.predict(test_data)
    
    return {"prediction": prediction}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)