# Sentiment and Emotion Analysis Application (Multilingual + Audio Support)



## Overview

This is a powerful, multilingual **Emotion Detection Web Application** built using **Flask**, **Machine Learning**, and **JavaScript**. It can:

- Detect emotions from user-inputted text in **any language** using translation
- Accept **speech input** via microphone and convert it to text
- Provide **Text-to-Speech (TTS)** output in the selected language
- Highlight the **dominant word** causing the emotion
- Visualize emotion predictions with interactive **Plotly pie charts**
- Copy input/output to clipboard
- Work seamlessly on both **desktop and mobile**

---

## 🔥 Key Features

### 🔤 Multilingual Text Input

- Supports over 100 languages using **Google Translate API**
- Automatically translates input text into English for emotion detection

### 🎤 Speech-to-Text Input

- Users can speak in their native language
- Uses browser-native SpeechRecognition API to transcribe

### 🔈 Text-to-Speech Output

- Converts final emotion response back into spoken audio
- Language-aware TTS with dynamic voice selection

### 📈 Real-Time Visualizations

- Interactive **Plotly pie chart** shows predicted emotion probabilities
- Highlights the most probable emotion distinctly

### 🧠 ML Model (Backend)

- Trained **Logistic Regression** classifier
- Feature extraction with **TfidfVectorizer**
- Trained on `text_emotion.csv` dataset

### 🧠 Dominant Word Detection

- Highlights the top influential word contributing to the emotion
- Uses vectorizer and model coefficients for interpretation

### 🖥️ UI/UX

- Fully responsive design using **HTML/CSS/JS + Bootstrap**
- Clipboard copy buttons for quick access
- Dropdown for language selection

---

## 💻 Tech Stack

### Frontend

- HTML5, CSS3, Bootstrap 5
- JavaScript (vanilla)
- Plotly.js for charts

### Backend

- Flask (Python)
- Googletrans for translation
- pyttsx3 for Text-to-Speech (offline)
- SpeechRecognition API (browser-based)
- Scikit-learn (LogisticRegression, TfidfVectorizer)

---

## 🚀 How It Works

1. **User Input**: User types or speaks any text (in any language)
2. **Translation**: Text is translated to English using Google Translate
3. **Emotion Detection**: ML model predicts the top 6 emotion probabilities
4. **Dominant Word**: The word most responsible for emotion is extracted
5. **TTS**: Predicted emotion is read aloud in the selected language
6. **Visualization**: Plotly pie chart shows emotion probabilities

---

## 📂 Project Structure

```bash
emotion-app/
├── app.py
├── requirements.txt
│
├── data/
│ ├── full_dataset/
│ │ ├── goemotions_1.csv
│ │ ├── goemotions_2.csv
│ │ └── goemotions_3.csv
│ ├── data.db
│ ├── processed_goemotions.csv
│ ├── train.tsv
│ ├── test.tsv
│
├── models/
│ └── trained_emotion_classifier.pkl
│
├── plots/
│ └── emotion_words.csv
│
├── scripts/
│ ├── preprocess_data.py
│ └── train_model.py
│
├── static/
│ ├── styles.css
│ ├── scripts.js
│ ├── mic-icon.png
│ ├── speaker-icon.png
│ └── copy-icon.png
│
├── templates/
│ └── index.html
├──README.md
```

---

## 🧪 Model Training (Optional)

If you want to train your own model:

1. Use `text_emotion.csv` dataset
2. Preprocess data (remove usernames, links, etc.)
3. Apply `TfidfVectorizer`
4. Train a `LogisticRegression` model
5. Save using `joblib` or `pickle`

---

## ✅ Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/Mahesh4037/Sentiment-and-Emotion-Analysis
cd Sentiment-and-Emotion-Analysis
```

2. **Install Requirements**

```bash
pip install -r requirements.txt
```

3. **Run the App**

```bash
python app.py
```

4. Open in browser:

```
http://localhost:5000
```

---

---

## 🧠 Model Info

- **Model**: Logistic Regression
- **Vectorizer**: TfidfVectorizer (max\_features=1000, stop\_words='english')
- **Dataset**: `text_emotion.csv` from Kaggle (multi-label text classification)
- **Emotions**: ['happy', 'sadness', 'anger', 'fear', 'surprise', 'neutral']

---

## 🌍 Supported Languages

- Hindi, English, Bengali, Punjabi, Marathi, Tamil, Telugu, Malayalam, Gujarati, Kannada, Urdu, and 100+ others
- Language dropdown available on the homepage

---

## 📌 License

This project is licensed under the **MIT License**.

---

## 📫 Contact

For queries or suggestions:

- Email: [ssingla2004@gmail.com](mailto\:ssingla2004@gmail.com)
- GitHub: [github.com/Mahesh4037](https://github.com/Mahesh4037)

---

## ⭐ Acknowledgements

- [Kaggle Datasets](https://www.kaggle.com/)
- [Google Translate](https://translate.google.com/)
- [Plotly JS](https://plotly.com/javascript/)
- [Flask Framework](https://flask.palletsprojects.com/)

---

## 🙏 Support

If you like this project, give it a ⭐ on GitHub. Contributions are welcome!

