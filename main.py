import cv2
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer
from light_controller import LightController


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    tracker = HandTracker(max_hands=1)
    recognizer = GestureRecognizer()
    light = LightController()

    print("Light Controller (ON/OFF + Brightness) started. Press 'Q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        # Flip webcam frame for mirror effect
        frame = cv2.flip(frame, 1)

        # Detect hands
        frame = tracker.find_hands(frame)

        # Get hand landmarks
        landmarks = tracker.get_landmark_positions(frame)

        gesture = "NONE"

        if landmarks:
            # Recognize gesture
            gesture = recognizer.recognize_gesture(landmarks)

            # Get index fingertip
            index_tip = landmarks[8]

            # Draw circle on index fingertip
            cv2.circle(
                frame,
                (index_tip[1], index_tip[2]),
                8,
                (255, 0, 255),
                cv2.FILLED
            )

            # -----------------------------------
            # Gesture -> Light Controller actions
            # -----------------------------------

            if gesture == "OPEN_PALM":
                light.turn_on()

            elif gesture == "FIST":
                light.turn_off()

            elif gesture == "PINCH":
                # Calculate thumb-index distance
                distance = recognizer.get_pinch_distance(landmarks)

                # Convert distance to brightness
                brightness = recognizer.distance_to_brightness(distance)

                # Set light brightness
                if brightness is not None:
                    light.set_brightness(brightness)

        # -----------------------------------
        # On-screen information panel
        # -----------------------------------

        status = light.get_status()

        # Black information panel
        cv2.rectangle(
            frame,
            (0, 0),
            (350, 160),
            (0, 0, 0),
            -1
        )

        # Gesture
        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        # Light ON/OFF status
        light_status_text = "ON" if status["on"] else "OFF"

        light_status_color = (
            (0, 255, 0)
            if status["on"]
            else (0, 0, 255)
        )

        cv2.putText(
            frame,
            f"Light: {light_status_text}",
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            light_status_color,
            2
        )

        # Brightness
        cv2.putText(
            frame,
            f"Brightness: {status['brightness']}%",
            (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        # Quit instruction
        cv2.putText(
            frame,
            "Press 'Q' to Quit",
            (10, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 200, 0),
            1
        )

        # Display window
        cv2.imshow(
            "Gesture Controlled Virtual Light Controller",
            frame
        )

        # Quit when Q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()