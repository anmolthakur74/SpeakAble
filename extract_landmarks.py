import os
import cv2
import csv
import mediapipe as mp

# Define input and output paths
DATA_DIR = 'data'
OUTPUT_CSV = 'landmark_data.csv'

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Prepare CSV header: 21 landmarks × (x, y, z) + label
header = []
for i in range(21):
    header.extend([f'x{i}', f'y{i}', f'z{i}'])
header.append('label')

# Open CSV file for writing landmark data
with open(OUTPUT_CSV, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    # Loop through each label folder (A–J)
    for label_folder in sorted(os.listdir(DATA_DIR)):
        folder_path = os.path.join(DATA_DIR, label_folder)
        if not os.path.isdir(folder_path):
            continue

        # Loop through each image in the folder
        for image_name in os.listdir(folder_path):
            if image_name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                image_path = os.path.join(folder_path, image_name)
                image = cv2.imread(image_path)
                if image is None:
                    print(f"[x] Failed to load image: {image_path}")
                    continue

                # Convert image to RGB for MediaPipe processing
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                result = hands.process(image_rgb)

                # If hand landmarks are detected, extract and store them
                if result.multi_hand_landmarks:
                    landmarks = result.multi_hand_landmarks[0].landmark
                    row = []
                    for lm in landmarks:
                        row.extend([lm.x, lm.y, lm.z])
                    row.append(label_folder.upper())
                    writer.writerow(row)
                    print(f"[✓] Processed {image_name} in {label_folder}/")
                else:
                    # Delete image if no hand is detected
                    print(f"[x] No hand detected in {image_name} (Label: {label_folder}) — DELETING")
                    os.remove(image_path)

print(f"\nLandmark extraction complete. Data saved to {OUTPUT_CSV}")
