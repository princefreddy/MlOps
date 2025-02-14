import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix, classification_report
)

def load_model_and_data(model_path, data_path):
    """Load saved model and test data"""
    saved_objects = joblib.load(model_path)
    model = saved_objects['model']
    scaler = saved_objects['scaler']
    label_encoder = saved_objects['label_encoder']
    
    # Load and prepare data
    df_cleaned = pd.read_csv(data_path)
    df_cleaned["SalePrice"] = pd.qcut(df_cleaned["SalePrice"], q=3, labels=["Low", "Medium", "High"])
    
    X = df_cleaned.drop(columns=["SalePrice"])
    y = df_cleaned["SalePrice"]
    
    # Scale features
    X_scaled = scaler.fit_transform(X)
    y_encoded = label_encoder.transform(y)
    
    return model, X_scaled, y_encoded, label_encoder

def evaluate_model(model, X_test, y_test, label_encoder):
    """Evaluate model performance"""
    # Predictions
    y_pred = model.predict(X_test)
    
    # Decode predictions back to original labels
    y_test_decoded = label_encoder.inverse_transform(y_test)
    y_pred_decoded = label_encoder.inverse_transform(y_pred)
    
    # Metrics calculation
    metrics = {
        'Accuracy': accuracy_score(y_test_decoded, y_pred_decoded),
        'Precision': precision_score(y_test_decoded, y_pred_decoded, average='weighted'),
        'Recall': recall_score(y_test_decoded, y_pred_decoded, average='weighted'),
        'F1 Score': f1_score(y_test_decoded, y_pred_decoded, average='weighted')
    }
    
    # Confusion Matrix
    cm = confusion_matrix(y_test_decoded, y_pred_decoded, labels=["Low", "Medium", "High"])
    
    return metrics, cm, y_test_decoded, y_pred_decoded

def plot_confusion_matrix(cm, labels):
    """Plot and save confusion matrix"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    plt.close()

def save_metrics(metrics):
    """Save evaluation metrics to a text file"""
    with open('model_metrics.txt', 'w') as f:
        for metric, value in metrics.items():
            f.write(f"{metric}: {value:.4f}\n")

def evaluation_pipeline(model_path='mlp_classifier_model.pkl', data_path='cleaned_data.csv'):
    """Complete model evaluation pipeline"""
    # Load model and data
    model, X_test, y_test, label_encoder = load_model_and_data(model_path, data_path)
    
    # Evaluate model
    metrics, cm, y_test_decoded, y_pred_decoded = evaluate_model(model, X_test, y_test, label_encoder)
    
    # Plot and save confusion matrix
    plot_confusion_matrix(cm, ["Low", "Medium", "High"])
    
    # Save metrics
    save_metrics(metrics)
    
    # Print detailed classification report
    print(classification_report(y_test_decoded, y_pred_decoded))

if __name__ == "__main__":
    evaluation_pipeline()
