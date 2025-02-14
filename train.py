import pandas as pd
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

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
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    ann_model = MLPClassifier(
        hidden_layer_sizes=(100, 50), 
        activation='relu', 
        solver='adam', 
        max_iter=500,
        random_state=42
    )
    ann_model.fit(X_train, y_train)

    return ann_model

def save_model(model, model_path='mlp_classifier_model.pkl'):
    """Save trained model and preprocessing objects"""
    joblib.dump({
        'model': model,
    }, model_path)

    print(f"Model saved to {model_path}")

def training_pipeline(data_path='cleaned_data.csv', model_path='mlp_classifier_model.pkl'):
    """Complete model training pipeline"""
    # Prepare data
    X, y = prepare_data(data_path)
    
    # Train model
    model = train_ann_model(X, y)
    
    # Save model and preprocessing objects
    save_model(model, model_path)

if __name__ == "__main__":
    training_pipeline()