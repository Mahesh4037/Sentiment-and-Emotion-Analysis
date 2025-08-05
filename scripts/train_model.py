import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

def preprocess_goemotions(csv_paths, output_path):
    """Combine and preprocess GoEmotions dataset."""
    # Load and concatenate the CSV files
    combined_df = pd.concat([pd.read_csv(path) for path in csv_paths], ignore_index=True)
    
    # Check for required columns
    if 'text' not in combined_df.columns:
        raise ValueError("Dataset must contain a 'text' column.")
    
    # Identify emotion columns (exclude 'text' and any other non-emotion columns)
    emotion_columns = [col for col in combined_df.columns if col not in ['text']]
    if not emotion_columns:
        raise ValueError("Dataset does not contain emotion labels.")
    
    # Ensure emotion columns are numeric
    combined_df[emotion_columns] = combined_df[emotion_columns].apply(pd.to_numeric, errors='coerce')
    
    # Handle rows where all emotion columns are NaN
    if combined_df[emotion_columns].isna().all(axis=1).any():
        print("Warning: Found rows with all NaN emotion values. These rows will be dropped.")
        combined_df = combined_df.dropna(subset=emotion_columns, how='all')
    
    # Combine one-hot encoded columns into a single 'emotion' column
    combined_df['emotion'] = combined_df[emotion_columns].idxmax(axis=1)
    
    # Drop unnecessary columns (retain only 'text' and 'emotion')
    combined_df = combined_df[['text', 'emotion']]
    
    # Remove rows with missing values
    combined_df.dropna(inplace=True)
    
    # Shuffle the dataset
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)
    
    # Save the processed dataset
    combined_df.to_csv(output_path, index=False)
    print(f"Processed dataset saved to {output_path}")
    return combined_df

def train_model(data_path, model_path):
    """Train the emotion classifier model."""
    # Load the preprocessed dataset
    df = pd.read_csv(data_path)
    
    # Check for required columns
    if 'text' not in df.columns or 'emotion' not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'emotion' columns.")
    
    # Extract features and labels
    X = df['text']
    y = df['emotion']

    # Define the model pipeline
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000)),
        ('clf', LogisticRegression(multi_class='multinomial', solver='lbfgs'))
    ])

    # Train the model
    pipe.fit(X, y)
    
    # Save the trained model
    joblib.dump(pipe, model_path)
    print(f"Model saved at {model_path}")

if __name__ == "__main__":
    input_paths = [
        "./data/full_dataset/goemotions_1.csv",
        "./data/full_dataset/goemotions_2.csv",
        "./data/full_dataset/goemotions_3.csv"
    ]
    output_file = "./data/processed_goemotions.csv"
    model_path = "./models/trained_emotion_classifier.pkl"

    # Preprocess the dataset and train the model
    processed_df = preprocess_goemotions(input_paths, output_file)
    train_model(output_file, model_path)
