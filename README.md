# Title: Real-Time Sign Language Recognition (Problem Statement 7)

# Project Name: SpeakAble

**SpeakAble** is an AI-powered real-time communication system designed to bridge the gap between individuals who are deaf, mute, or blind. It combines gesture recognition, speech-to-text, and text-to-speech to enable inclusive, accessible conversations.

---

## Project Objectives

- Recognize hand gestures using computer vision and machine learning
- Convert recognized gestures into text and speech
- Convert spoken audio into text in real-time
- Enable communication between deaf, mute, and blind users

---

## Demo Video

Watch the project demo here:  
[Demo Video Link](https://drive.google.com/file/d/19K0c7B-3wHCzISheGRyOPX4ge4ACASNq/view?usp=sharing)

---

## Features

- Real-time hand gesture recognition (letters, commands like `space`, `del`, `end`)
- Speech-to-text input for blind-to-mute communication
- Text-to-speech output for mute-to-blind interaction
- Stable prediction buffering and autocorrect
- Clean UI with live output overlay

---

## Technologies Used

- **Python**
- **OpenCV**, **MediaPipe** – Hand tracking
- **scikit-learn**, **joblib** – Gesture classification
- **pyttsx3** – Text-to-speech (offline)
- **SpeechRecognition**, **PyAudio** – Speech-to-text
- **TensorFlow / MLP / XGBoost** – Model training

---

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/anmolthakur74/SpeakAble-Project.git
cd SpeakAble-Project
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

## 📝 Requirements

- Python 3.8+
- Webcam
- Microphone (for speech input)
- Windows/Linux

---

## Author

**Anmol Thakur**  

🔗 [LinkedIn](https://www.linkedin.com/in/anmolthakur74)  
🔗 [GitHub](https://github.com/anmolthakur74)

---

## Acknowledgements

- MediaPipe by Google for hand tracking
- Scikit-learn, TensorFlow, OpenCV, Pyttsx3
- Voice and gesture recognition resources from open-source community
