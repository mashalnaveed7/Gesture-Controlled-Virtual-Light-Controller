import math


class GestureRecognizer:
    def __init__(self):
        # Landmark IDs for fingertips and their corresponding lower joints
        self.tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    def get_finger_states(self, landmarks):
        """
        Returns a list of 5 values (0 or 1) representing whether
        each finger is extended (1) or folded (0).

        Order: [Thumb, Index, Middle, Ring, Pinky]
        """
        if not landmarks or len(landmarks) < 21:
            return []

        fingers = []

        # -----------------------------------
        # Thumb (distance-based, orientation-agnostic)
        # -----------------------------------

        pinky_mcp = landmarks[17]
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        dist_tip = math.hypot(
            thumb_tip[1] - pinky_mcp[1],
            thumb_tip[2] - pinky_mcp[2]
        )

        dist_ip = math.hypot(
            thumb_ip[1] - pinky_mcp[1],
            thumb_ip[2] - pinky_mcp[2]
        )

        fingers.append(1 if dist_tip > dist_ip else 0)

        # -----------------------------------
        # Other 4 fingers
        # Distance-based detection using wrist
        # -----------------------------------

        wrist = landmarks[0]

        for i in range(1, 5):
            tip = landmarks[self.tip_ids[i]]
            pip = landmarks[self.tip_ids[i] - 2]

            # Distance from fingertip to wrist
            dist_tip = math.hypot(
                tip[1] - wrist[1],
                tip[2] - wrist[2]
            )

            # Distance from PIP joint to wrist
            dist_pip = math.hypot(
                pip[1] - wrist[1],
                pip[2] - wrist[2]
            )

            # Finger is considered extended when the fingertip
            # is sufficiently farther from the wrist than the PIP joint
            fingers.append(
                1 if dist_tip > dist_pip * 1.1 else 0
            )

        return fingers

    def get_pinch_distance(self, landmarks):
        """
        Calculates Euclidean distance between thumb tip (id 4)
        and index fingertip (id 8).

        Returns None if landmarks are unavailable.
        """
        if not landmarks or len(landmarks) < 21:
            return None

        x1, y1 = landmarks[4][1], landmarks[4][2]
        x2, y2 = landmarks[8][1], landmarks[8][2]

        distance = math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

        return distance

    def distance_to_brightness(
        self,
        distance,
        min_dist=15,
        max_dist=150
    ):
        """
        Converts thumb-index distance into a brightness percentage (0-100).

        min_dist = fingers touching (0% brightness)
        max_dist = fingers spread apart, thumb/index still extended (100% brightness)
        """
        if distance is None:
            return None

        # Keep distance within the allowed range
        distance = max(
            min_dist,
            min(max_dist, distance)
        )

        # Convert distance to brightness percentage
        brightness = (
            (distance - min_dist) /
            (max_dist - min_dist)
        ) * 100

        return int(brightness)

    def recognize_gesture(self, landmarks):
        """
        Returns a gesture label string based on finger states.

        Currently supports:
        OPEN_PALM, FIST, INDEX, PINCH, TWO_FINGERS
        """
        fingers = self.get_finger_states(landmarks)

        if not fingers:
            return "NONE"

        total_extended = sum(fingers)

        # -----------------------------------
        # Fist
        # -----------------------------------
        # All fingers folded
        if total_extended == 0:
            return "FIST"

        # -----------------------------------
        # Pinch
        # -----------------------------------
        # Thumb + index extended
        # Middle + ring + pinky folded
        if (
            fingers[0] == 1 and
            fingers[1] == 1 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        ):
            return "PINCH"

        # -----------------------------------
        # Two Fingers
        # -----------------------------------
        # Index + middle extended
        # Thumb + ring + pinky folded
        if (
            fingers[1] == 1 and
            fingers[2] == 1 and
            fingers[0] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        ):
            return "TWO_FINGERS"

        # -----------------------------------
        # Index
        # -----------------------------------
        # Only index finger extended
        if (
            fingers[1] == 1 and
            fingers[0] == 0 and
            fingers[2] == 0 and
            fingers[3] == 0 and
            fingers[4] == 0
        ):
            return "INDEX"

        # -----------------------------------
        # Open Palm
        # -----------------------------------
        # Four or more fingers extended
        if total_extended >= 4:
            return "OPEN_PALM"

        # -----------------------------------
        # Unknown gesture
        # -----------------------------------
        return "UNKNOWN"