import cv2
import numpy as np
import mediapipe as mp
import pyttsx3
import joblib
import speech_recognition as sr
from collections import deque, Counter
import threading
import time

# Load model and preprocessing tools
model = joblib.load('final_stack_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Text-to-speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Speech-to-text
def listen_and_set_text():
    global blind_to_mute_text, turn_flag
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening from user")
            audio = r.listen(source, timeout=2, phrase_time_limit=10)
            blind_to_mute_text = r.recognize_google(audio)
            print("Heard:", blind_to_mute_text)
            turn_flag = True  # Signal to deaf/mute user to respond
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
        blind_to_mute_text = "No speech"
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        blind_to_mute_text = "Could not understand"
    except sr.RequestError:
        print("API unavailable or no internet.")
        blind_to_mute_text = "Speech recognition error"

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

# Buffers and variables
prediction_buffer = deque(maxlen=15)
confirmed_pred = ""
current_word = ""
sentence_buffer = ""
blind_to_mute_text = ""
turn_flag = False
cooldown_time = 1.2  # seconds
last_confirmed_time = time.time() - cooldown_time

# Layout
output_width = 960
output_height = 480
cam_width = int(output_width * 0.7)
side_width = output_width - cam_width

# UI helper
def put_label(img, text, y, color=(255, 255, 255), font_scale=0.6):
    cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (cam_width, output_height))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    current_time = time.time()

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        landmarks = [coord for lm in hand_landmarks.landmark for coord in (lm.x, lm.y, lm.z)]

        if len(landmarks) == 63:
            X = scaler.transform([landmarks])
            pred = model.predict(X)
            label = label_encoder.inverse_transform(pred)[0]
            prediction_buffer.append(label)

            if len(prediction_buffer) == prediction_buffer.maxlen and current_time - last_confirmed_time > cooldown_time:
                most_common = Counter(prediction_buffer).most_common(1)[0]
                if most_common[1] > 12:
                    confirmed_pred = most_common[0]
                    last_confirmed_time = current_time

                    if confirmed_pred.lower() == 'space':
                        sentence_buffer += current_word + " "
                        current_word = ""
                    elif confirmed_pred.lower() == 'del':
                        current_word = current_word[:-1]
                    elif confirmed_pred.lower() == 'end':
                        sentence_buffer += current_word
                        speak(sentence_buffer)
                        current_word = ""
                        sentence_buffer = ""
                        turn_flag = False  # Turn over after response
                    else:
                        current_word += confirmed_pred

                    prediction_buffer.clear()

        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Side panel
    side_panel = np.zeros((output_height, side_width, 3), dtype=np.uint8)
    put_label(side_panel, f"Predicted Letter: {confirmed_pred}", 50, (0, 255, 255))
    put_label(side_panel, f"Current Word: {current_word}", 100, (255, 255, 0))
    put_label(side_panel, "Final Sentence:", 150, (0, 255, 0))
    put_label(side_panel, sentence_buffer[-30:], 180, (0, 255, 0))

    # Show full speech input (wrapped)
    put_label(side_panel, "Speech Input:", 230, (255, 100, 100))
    lines = blind_to_mute_text.strip().split(' ')
    display_text = ""
    line = ""
    for word in lines:
        if len(line + word) < 25:
            line += word + ' '
        else:
            display_text += line + "\n"
            line = word + ' '
    display_text += line

    y_offset = 260
    for l in display_text.strip().split('\n'):
        put_label(side_panel, l, y_offset, (255, 100, 100))
        y_offset += 30

    # Turn signal
    if turn_flag:
        put_label(side_panel, "Your turn to sign!", y_offset + 20, (0, 255, 255), font_scale=0.7)

    full_display = np.hstack((frame, side_panel))
    cv2.imshow("Sign-Speech Communication UI", full_display)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == 13:  # ENTER
        sentence_buffer += current_word
        speak(sentence_buffer)
        current_word = ""
        sentence_buffer = ""
        threading.Thread(target=listen_and_set_text, daemon=True).start()
    elif key == 8:  # BACKSPACE
        current_word = current_word[:-1]
    elif key == 32:  # SPACE
        sentence_buffer += current_word + " "
        current_word = ""

cap.release()
cv2.destroyAllWindows()
