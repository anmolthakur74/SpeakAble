import cv2
import os

# Define the root directory where image data will be stored
DATA_DIR = 'data'

# Acceptable labels: A–Z letters or gesture keywords
valid_labels = [chr(i) for i in range(65, 91)] + ['PALM', 'THUMBS_UP', 'THUMBS_DOWN']

# Prompt user to input the sign label
label = input("Enter the sign label (A–Z or palm, thumbs_up, thumbs_down): ").strip().upper()

# Validate input
if label not in valid_labels:
    print("Error: Please enter a single letter (A–Z) or one of: palm, thumbs_up, thumbs_down.")
    exit()

# Create a directory for the current label if it doesn't exist
save_dir = os.path.join(DATA_DIR, label)
os.makedirs(save_dir, exist_ok=True)

# Count existing images to continue image numbering from the last saved
existing_images = [f for f in os.listdir(save_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
count = len(existing_images)

# Initialize webcam feed
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

print(f"\nCapturing images for label '{label}'")
print("Press 's' to save image | Press 'q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break

    # Flip the frame horizontally for mirror-like interaction
    frame = cv2.flip(frame, 1)

    # Display label and image count on the screen
    cv2.putText(frame, f"Label: {label} | Count: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the live feed window
    cv2.imshow("Sign Capture", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        # Save the current frame as an image file
        count += 1
        filename = f"{label}_{count}.jpg"
        cv2.imwrite(os.path.join(save_dir, filename), frame)
        print(f"Saved: {filename}")
    elif key == ord('q'):
        # Exit loop on 'q' key press
        break

# Release webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
print(f"\nDone. Total images for '{label}': {count}")