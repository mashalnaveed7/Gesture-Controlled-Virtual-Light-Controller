import cv2
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer
from light_controller import LightController
from virtual_room import VirtualRoom


def main():
    print("CHECKPOINT 1: Starting webcam...")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("CHECKPOINT 2: Webcam opened. Initializing tracker/recognizer...")

    tracker = HandTracker(max_hands=1)
    recognizer = GestureRecognizer()

    print("CHECKPOINT 3: Creating VirtualRoom (Pygame window)...")

    room = VirtualRoom(1280, 720)

    print("CHECKPOINT 4: VirtualRoom created successfully.")

    room_area_w = room.room_w
    room_area_h = room.height - room.header_h - room.footer_h

    light = LightController(
        screen_width=room_area_w,
        screen_height=room_area_h
    )

    light.set_position(
        room_area_w // 2,
        room_area_h // 2
    )

    print("CHECKPOINT 5: Entering main loop...")

    previous_gesture = "NONE"
    fps = 0

    running = True

    while running:
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

            # Draw fingertip marker
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

                if brightness is not None:
                    light.set_brightness(brightness)

            elif gesture == "INDEX":
                # Convert webcam coordinates to room coordinates
                frame_h, frame_w = frame.shape[:2]

                room_x = int(
                    (index_tip[1] / frame_w) * room_area_w
                )

                room_y = int(
                    (index_tip[2] / frame_h) * room_area_h
                )

                # Move virtual light
                light.set_position(room_x, room_y)

            elif gesture == "TWO_FINGERS":
                # Change color only once when gesture first appears
                if previous_gesture != "TWO_FINGERS":
                    light.next_color()

            # Store current gesture for next frame
            previous_gesture = gesture

        # -----------------------------------
        # Get current light status
        # -----------------------------------

        status = light.get_status()

        # -----------------------------------
        # Convert light position to display coordinates
        # -----------------------------------

        display_status = dict(status)

        display_status["position"] = [
            status["position"][0] + room.cam_w,
            status["position"][1] + room.header_h
        ]

        # -----------------------------------
        # Virtual Room events and rendering
        # -----------------------------------

        running = room.handle_events()

        fps = room.tick(30)

        room.render(
            frame,
            gesture,
            display_status,
            fps
        )

    # -----------------------------------
    # Cleanup
    # -----------------------------------

    cap.release()
    room.quit()


if __name__ == "__main__":
    import traceback

    try:
        main()

    except Exception as e:
        print("=== CRASH DETECTED ===")
        traceback.print_exc()
        input("Press Enter to exit...")