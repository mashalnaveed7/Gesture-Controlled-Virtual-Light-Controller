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

    print("Light Controller (ON/OFF) started. Press 'Q' to quit.")

    while True:
        success, frame = cap.read()

        if not success:
            print("Error: Failed to read frame from webcam.")
            break

        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)
        landmarks = tracker.get_landmark_positions(frame)

        gesture = "NONE"

        if landmarks:
            gesture = recognizer.recognize_gesture(landmarks)

            index_tip = landmarks[8]
            cv2.circle(frame, (index_tip[1], index_tip[2]), 8, (255, 0, 255), cv2.FILLED)

            # --- Gesture -> Light Controller actions ---
            if gesture == "OPEN_PALM":
                light.turn_on()
            elif gesture == "FIST":
                light.turn_off()

        # --- On-screen info panel ---
        status = light.get_status()

        cv2.rectangle(frame, (0, 0), (350, 130), (0, 0, 0), -1)

        cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        light_status_text = "ON" if status["on"] else "OFF"
        light_status_color = (0, 255, 0) if status["on"] else (0, 0, 255)
        cv2.putText(frame, f"Light: {light_status_text}", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, light_status_color, 2)

        cv2.putText(frame, "Press 'Q' to Quit", (10, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)

        cv2.imshow("Gesture Controlled Virtual Light Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()