import pandas as pd
import numpy as np
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

def prepare_data(data_path):
    """Load and prepare data for training"""
    df_cleaned = pd.read_csv(data_path)
    
    # Convert SalePrice to categories
    df_cleaned["SalePrice"] = pd.qcut(df_cleaned["SalePrice"], q=3, labels=["Low", "Medium", "High"])
    
    X = df_cleaned.drop(columns=["SalePrice"])
    y = df_cleaned["SalePrice"]
    
    return X, y

def train_ann_model(X, y):
    """Train Artificial Neural Network Model"""
    # Normalisation des features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Encodage des labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)
    
    # Initialisation du modèle
    ann_model = MLPClassifier(
        hidden_layer_sizes=(100, 50), 
        activation='relu', 
        solver='adam', 
        max_iter=500,
        random_state=42
    )
    
    # Entraînement du modèle
    ann_model.fit(X_train, y_train)
    
    return ann_model, X_test, y_test, le

def save_model(model, scaler, label_encoder, model_path='mlp_classifier_model.pkl'):
    """Save trained model and preprocessing objects"""
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'label_encoder': label_encoder
    }, model_path)
    print(f"Model saved to {model_path}")

def training_pipeline(data_path='cleaned_data.csv', model_path='mlp_classifier_model.pkl'):
    """Complete model training pipeline"""
    # Prepare data
    X, y = prepare_data(data_path)
    
    # Train model
    model, X_test, y_test, label_encoder = train_ann_model(X, y)
    
    # Save model
    save_model(model, StandardScaler(), label_encoder, model_path)

if __name__ == "__main__":
    training_pipeline()
