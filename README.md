## Project Name: SpeakAble

**SpeakAble** is an AI-driven real-time communication system that bridges the gap for people with sensory impairments, including visual, hearing, and speech impairments. It uses gesture recognition, speech-to-text, and text-to-speech to enable inclusive, accessible conversations.

---

## Project Objectives

- Recognize hand gestures using computer vision and machine learning
- Convert recognized gestures into text and speech
- Convert spoken audio into text in real-time
- Enables communication between users with hearing, speech, and visual impairments

---

## Features

- Real-time hand gesture recognition
- Speech-to-text enabling blind-to-non-verbal communication
- Text-to-speech enabling non-verbal-to-blind interaction
- Stable prediction buffering and autocorrect
- Clean UI with live output overlay

---

## Technologies Used

- **Python** – Core language
- **OpenCV** & **MediaPipe** – Real-time hand tracking via webcam
- **scikit-learn** & **joblib** – Model training and serialization
- **TensorFlow**, **XGBoost**, **MLPClassifier** – Ensemble gesture classification
- **pyttsx3** – Offline Text-to-Speech output
- **SpeechRecognition** & **PyAudio** – Online Speech-to-Text using Google Web Speech API

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/anmolthakur74/SpeakAble.git
cd SpeakAble
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv gesture_env
gesture_env\Scripts\activate  # For Windows
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the gesture recognition app

```bash
python predict_webcam.py
```

---

## Requirements

- Python 3.8+
- Webcam
- Microphone (for speech input)
- Windows/Linux

---

## Author

**Anmol Thakur**  

[LinkedIn](https://www.linkedin.com/in/anmolthakur74)  
[GitHub](https://github.com/anmolthakur74)

---

## Acknowledgements

- MediaPipe by Google for hand tracking
- Scikit-learn, TensorFlow, OpenCV, Pyttsx3
- Voice and gesture recognition resources from open-source community
