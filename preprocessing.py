import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import RandomOverSampler

def load_data(train_path, test_path):
    """Load training and test datasets"""
    train_data = pd.read_csv(train_path)
    test_data = pd.read_csv(test_path)
    return train_data, test_data

def handle_missing_values(train_data):
    """Remove columns with >50% missing values and fill remaining with most frequent value"""
    missing_percentage = train_data.isnull().mean() * 100
    columns_to_drop = missing_percentage[missing_percentage > 50].index.tolist()
    train_data_cleaned = train_data.drop(columns=columns_to_drop)
    train_data_cleaned = train_data_cleaned.apply(lambda x: x.fillna(x.value_counts().index[0]))
    return train_data_cleaned

def reduce_dimensionality(train_data):
    """Apply PCA for dimensionality reduction"""
    X = train_data.drop(columns=["SalePrice"])
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object", "category"]).columns

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
    ])

    df_transformed = preprocessor.fit_transform(train_data)

    pca = PCA(n_components=0.95, svd_solver="full")
    df_pca = pca.fit_transform(df_transformed)

    return df_pca, train_data["SalePrice"]

def oversample_data(X, y):
    """Apply random oversampling to balance the dataset"""
    ros = RandomOverSampler(sampling_strategy='auto', random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X, y)
    
    return X_resampled, y_resampled

def preprocess_pipeline(train_path, test_path, output_path):
    """Complete preprocessing pipeline"""
    # Load data
    train_data, test_data = load_data(train_path, test_path)
    
    # Handle missing values
    train_data_cleaned = handle_missing_values(train_data)
    
    # Reduce dimensionality
    X_pca, y = reduce_dimensionality(train_data_cleaned)
    
    # Oversample data
    X_resampled, y_resampled = oversample_data(X_pca, y)
    
    # Create final dataframe
    df_resampled = pd.DataFrame(X_resampled, columns=[f'feature_{i}' for i in range(X_resampled.shape[1])])
    df_resampled['SalePrice'] = y_resampled
    
    # Save preprocessed data
    df_resampled.to_csv(output_path, index=False)
    
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_pipeline("train.csv", "test.csv", "cleaned_data.csv")
