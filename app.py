import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from flask import Flask, render_template, request, jsonify
from googletrans import Translator


# Initialize Flask App
app = Flask(__name__)

# Paths
MODEL_PATH = "./models/trained_emotion_classifier.pkl"
TRAIN_DATA_PATH = "./data/train.tsv"

emotion_words_df = pd.read_csv("plots/emotion_words.csv")  # Using a raw string


# Function to read TSV file
def read_tsv(path):
    return pd.read_csv(path, sep='\t', encoding='utf-8', on_bad_lines='skip')

# Load the training dataset
df = read_tsv(TRAIN_DATA_PATH)

# Check if the dataset has the required columns
if 'text' not in df.columns or 'label' not in df.columns:
    raise ValueError("Dataset must contain 'text' and 'label' columns.")

# Emotion mapping
emotion_mapping = {
    0: "admiration", 1: "amusement", 2: "anger", 3: "annoyance", 4: "approval",
    5: "caring", 6: "confusion", 7: "curiosity", 8: "desire", 9: "disappointment",
    10: "disapproval", 11: "disgust", 12: "embarrassment", 13: "excitement", 14: "fear",
    15: "gratitude", 16: "grief", 17: "joy", 18: "love", 19: "nervousness", 20: "optimism",
    21: "pride", 22: "realization", 23: "relief", 24: "remorse", 25: "sadness", 26: "surprise", 27: "neutral"
}

# Map labels to emotions
df['emotion'] = df['label'].map(emotion_mapping)

# Train or load model
def train_model():
    """Train and save the emotion classifier model."""
    X = df['text']
    y = df['emotion']
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000)),
        ('clf', LogisticRegression(multi_class='multinomial', solver='lbfgs'))
    ])
    model.fit(X, y)
    os.makedirs("./models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

# Load existing model or train a new one
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = train_model()

# Create a mapping of emotion -> words
emotion_word_map = emotion_words_df.groupby("emotion")["word"].apply(list).to_dict()

def get_dominant_words(text, emotion=None):
    words = text.lower().split()  # Simple split, you can use a tokenizer
    dominant_words = {}
    
    # If emotion is provided, filter by it; otherwise, return words for all emotions
    if emotion:
        emotion_words = set(emotion_word_map.get(emotion, []))
        dominant_words[emotion] = list(set(word for word in words if word in emotion_words))
    else:
        for emotion, words_list in emotion_word_map.items():
            matching_words = list(set(word for word in words if word in words_list))
            if matching_words:
                dominant_words[emotion] = matching_words
    
    return dominant_words


# Utility functions for prediction
def predict_emotions(text):
    return model.predict([text])[0]

def get_prediction_proba(text):
    probabilities = model.predict_proba([text])[0]
    return dict(zip(model.classes_, probabilities))

# Routes
@app.route("/")
def home():
    """Render the main page."""
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    """Translate text to the specified language."""
    data = request.get_json()
    text = data.get("text", "")
    language = data.get("language", "en")
    if not text or not language:
        return jsonify({"error": "Invalid input"}), 400
    translator = Translator()
    translated = translator.translate(text, dest=language)
    return jsonify({"translated_text": translated.text})

@app.route("/analyze-feedback", methods=["POST"])
def analyze_feedback():
    """Analyze feedback for emotion detection and show dominant words."""    
    data = request.get_json()
    feedback = data.get("feedback", "")
    if feedback:
        # Predict the emotion and probabilities
        prediction = predict_emotions(feedback)
        probabilities = get_prediction_proba(feedback)

        # Get dominant words associated with all emotions
        dominant_words = get_dominant_words(feedback)

        return jsonify({
            "feedback_type": prediction,
            "emotion_score": max(probabilities.values()),
            "probabilities": probabilities,
            "dominant_words": dominant_words  # Include all dominant words for each emotion
        })
    return jsonify({"error": "No feedback provided"}), 400



if __name__ == "__main__":
    app.run(debug=True)
