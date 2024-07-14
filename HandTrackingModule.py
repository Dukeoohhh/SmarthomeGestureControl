import cv2
import time
import numpy as np
import mediapipe as mp
import pickle
from sklearn.neural_network import MLPClassifier
from RoomElement import Room

from google.protobuf import message_factory as _message_factory

SystemStatus = False


def Handful():
    global SystemStatus
    if not SystemStatus:
        print("Smart Home Gesture Detection System On.")
        SystemStatus = True
    else:
        print("Smart Home Gesture Detection System Off.")
        SystemStatus = False


def GestureControl(gesture, room):
    global SystemStatus
    if gesture == 'Handful':
        Handful()

    if SystemStatus:
        if gesture == 'One_Fingers':
            room.light_controll()
        elif gesture == 'Two_Fingers':
            room.air_conditioner_controll()
        elif gesture == 'Three_Fingers':
            room.fan_controll()
        elif gesture == 'Four_Fingers':
            room.curtain_controll()
        elif gesture == 'Five_Fingers':
            room.curtain_controll()


def main():
    # Load MLP Model for classify hand gestures
    mlpModel = MLPClassifier()
    with open('Model/MLP.pkl', 'rb') as f:
        mlp = pickle.load(f)
    mlpModel = mlp

    # Initialize Mediapipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Timer and counter for detecting hands
    hand_detected_start_time = None
    hand_detected_duration = 0
    hand_detected_threshold = 3  # seconds

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

            # Always draw the hand landmarks and connections
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_detected_duration >= hand_detected_threshold:
                for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                    # Print landmark coordinates to the console
                    landmark_coordinate = []
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        landmark_coordinate.append(landmark.x)
                        landmark_coordinate.append(landmark.y)
                        landmark_coordinate.append(landmark.z)

                    # Convert and reshape data
                    landmark_coordinate = np.array(landmark_coordinate).reshape(1, -1)
                    gesture = mlpModel.predict(landmark_coordinate)[0]

                    # Send gesture and room to control Smart Home System
                    GestureControll(gesture, Room1)

                # Reset the timer and duration after printing
                hand_detected_start_time = None
                hand_detected_duration = 0
            else:
                # Calculate remaining time
                remaining_time = hand_detected_threshold - hand_detected_duration
                cv2.putText(frame, f"Hold still: {int(remaining_time + 1)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 255, 0), 3, cv2.LINE_AA)
        else:
            # Reset the timer and duration if no hand is detected
            hand_detected_start_time = None
            hand_detected_duration = 0

        # Display the frame
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
