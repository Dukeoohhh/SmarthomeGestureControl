import cv2
import time
import numpy as np
import mediapipe as mp
import pickle
from RoomElement import Room
from sklearn.neural_network import MLPClassifier
import warnings

SystemStatus = False

def Handful():
    global SystemStatus
    if not SystemStatus:
        print("::[System] >> Smart Home Gesture Detection System On.", end='\n\n')
        SystemStatus = True
    else:
        print("::[System] >> Smart Home Gesture Detection System Off.", end='\n\n')
        SystemStatus = False

def GestureControl(gesture, room):
    global SystemStatus
    if gesture == 'Handful':
        Handful()

    if SystemStatus:
        if gesture == 'One_Fingers':
            room.light_control()
        elif gesture == 'Two_Fingers':
            room.air_conditioner_control()
        elif gesture == 'Three_Fingers':
            room.fan_control()
        elif gesture == 'Four_Fingers':
            room.curtain_control()
        elif gesture == 'Five_Fingers':
            room.music_control()
        elif gesture == 'OK':
            room.light_color_control()
        elif gesture == 'Thumb':
            room.tv_control()

def main():
    # Load MLP Model for classifying hand gestures
    with open('MLP.pkl', 'rb') as f:
        mlpModel = pickle.load(f)

    # Disable all warnings
    warnings.filterwarnings("ignore")

    # Initialize Mediapipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Timer and counter for detecting hands
    hand_detected_start_time = None
    hand_detected_duration = 0
    hand_detected_threshold = 2  # seconds
    gesture_delay = 4  # seconds delay after gesture
    gesture_time = 0  # Timer for gesture delay

    # Create room class
    Room1 = Room("Bedroom")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image horizontally
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and detect hands
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            if hand_detected_start_time is None:
                hand_detected_start_time = time.time()

            hand_detected_duration = time.time() - hand_detected_start_time

            # Draw the hand landmarks and connections
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_detected_duration >= hand_detected_threshold:
                if time.time() - gesture_time >= gesture_delay:  # Check if enough time has passed
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Extract landmark coordinates
                        landmark_coordinate = []
                        for idx, landmark in enumerate(hand_landmarks.landmark):
                            landmark_coordinate.append(landmark.x)
                            landmark_coordinate.append(landmark.y)
                            landmark_coordinate.append(landmark.z)

                        # Convert and reshape data
                        landmark_coordinate = np.array(landmark_coordinate).reshape(1, -1)
                        gesture = mlpModel.predict(landmark_coordinate)[0]

                        # Send gesture and room to control Smart Home System
                        GestureControl(gesture, Room1)

                    # Set delay for 2 seconds
                    gesture_time = time.time()

                # Reset the timer and duration after printing
                hand_detected_start_time = None
                hand_detected_duration = 0
            else:
                remaining_time = hand_detected_threshold - hand_detected_duration
                cv2.putText(frame, f"Hold still: {int(remaining_time + 1)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 0), 3, cv2.LINE_AA)
        else:
            hand_detected_start_time = None
            hand_detected_duration = 0

        # Check if in gesture delay period
        if time.time() - gesture_time < gesture_delay:
            cv2.putText(frame, f"Waiting: {int(gesture_delay - (time.time() - gesture_time))}", (10, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
