import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Define gesture recognition function
def recognize_gesture(landmarks):
    # Calculate distances between landmarks for gesture recognition
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Check for specific gestures based on the individual finger tips' position

    # Thumb gesture (Play/Pause)
    if thumb_tip.y < index_tip.y and thumb_tip.y < middle_tip.y and thumb_tip.y < ring_tip.y and thumb_tip.y < pinky_tip.y:
        return "play_pause"  # Thumb triggers play/pause

    # Index finger gesture (Volume Up)
    if index_tip.y < thumb_tip.y and index_tip.y < middle_tip.y and index_tip.y < ring_tip.y and index_tip.y < pinky_tip.y:
        return "volume_up"  # Index finger triggers volume up

    # Middle finger gesture (Volume Down)
    if middle_tip.y < thumb_tip.y and middle_tip.y < index_tip.y and middle_tip.y < ring_tip.y and middle_tip.y < pinky_tip.y:
        return "volume_down"  # Middle finger triggers volume down

    # Ring finger gesture (Skip Forward)
    if ring_tip.y < thumb_tip.y and ring_tip.y < index_tip.y and ring_tip.y < middle_tip.y and ring_tip.y < pinky_tip.y:
        return "skip_forward"  # Ring finger triggers skip forward

    # Pinky finger gesture (Skip Backward)
    if pinky_tip.y < thumb_tip.y and pinky_tip.y < index_tip.y and pinky_tip.y < middle_tip.y and pinky_tip.y < ring_tip.y:
        return "skip_backward"  # Pinky finger triggers skip backward

    return None  # No gesture recognized

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the image
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize gestures
            gesture = recognize_gesture(hand_landmarks.landmark)
            if gesture == "play_pause":
                pyautogui.press('space')
            elif gesture == "volume_up":
                pyautogui.press('volumeup')
            elif gesture == "volume_down":
                pyautogui.press('volumedown')
            elif gesture == "skip_forward":
                pyautogui.press('right')
            elif gesture == "skip_backward":
                pyautogui.press('left')

    # Display the resulting frame
    cv2.imshow('Hand Gesture Control', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()