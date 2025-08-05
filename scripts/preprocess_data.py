import pandas as pd
from sklearn.model_selection import train_test_split
import os
import json

# Paths
DATASET_PATH = "data/dataset/goemotions.csv"
PROCESSED_DATA_DIR = "data/processed"
LABEL_MAPPING_PATH = "data/processed/label_mapping.json"

# Create directories if not exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def preprocess_data():
    """Preprocess the GoEmotions dataset for the emotion classification model."""
    # Load the dataset
    try:
        df = pd.read_csv(DATASET_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Ensure the file is placed correctly.")

    # Check required columns
    required_columns = ["text", "emotion"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Dataset must contain the following columns: {required_columns}")

    # Map emotions to numerical labels
    emotions = df["emotion"].unique()
    emotion_to_label = {emotion: idx for idx, emotion in enumerate(emotions)}
    label_to_emotion = {idx: emotion for emotion, idx in emotion_to_label.items()}

    # Save the mapping for model and inference use
    with open(LABEL_MAPPING_PATH, "w") as f:
        json.dump(label_to_emotion, f)

    # Map emotions to numerical labels in the dataset
    df["label"] = df["emotion"].map(emotion_to_label)

    # Split into training, validation, and test sets
    train_df, temp_df = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df["label"], random_state=42)

    # Save processed datasets
    train_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "train.csv"), index=False)
    val_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "val.csv"), index=False)
    test_df.to_csv(os.path.join(PROCESSED_DATA_DIR, "test.csv"), index=False)

    print("Data preprocessing complete.")
    print(f"Train set size: {len(train_df)}")
    print(f"Validation set size: {len(val_df)}")
    print(f"Test set size: {len(test_df)}")

if __name__ == "__main__":
    preprocess_data()
