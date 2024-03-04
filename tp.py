import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# For drawing hand landmarks on the captured video frames.
mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture.
cap = cv2.VideoCapture(0)

# Variables to store position and movement.
prev_x = 0
gesture_threshold = 100  # Threshold to detect swipe gesture.

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty frame.")
        continue

    # Flip the frame horizontally for a later selfie-view display, and convert the BGR image to RGB.
    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    # Pass frame to MediaPipe Hands.
    results = hands.process(frame)

    # Draw hand landmarks.
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Calculate the current x position of the hand.
            curr_x = sum([lm.x for lm in hand_landmarks.landmark]) / len(hand_landmarks.landmark)
            curr_x *= frame.shape[1]

    # Detect swipe gestures.
    if prev_x:
        diff = curr_x - prev_x
        if diff > gesture_threshold:
            print("Swipe Right: Switching tab to the right.")
            pyautogui.hotkey('ctrl', 'tab')  # Simulate CTRL+Tab
        elif diff < -gesture_threshold:
            print("Swipe Left: Switching tab to the left.")
            pyautogui.hotkey('ctrl', 'shift', 'tab')  # Simulate CTRL+Shift+Tab

    prev_x = curr_x if 'curr_x' in locals() else 0

    # Display the frame.
    cv2.imshow('Swipe to Switch Tabs', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release resources.
cap.release()
cv2.destroyAllWindows()
