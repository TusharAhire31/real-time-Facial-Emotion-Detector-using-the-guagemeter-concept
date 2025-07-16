def detect_blinks(landmarks, shape):
    try:
        height, width, _ = shape

        left_eye_top = landmarks.landmark[159].y
        left_eye_bottom = landmarks.landmark[145].y
        right_eye_top = landmarks.landmark[386].y
        right_eye_bottom = landmarks.landmark[374].y

        left_eye_gap = abs(left_eye_top - left_eye_bottom)
        right_eye_gap = abs(right_eye_top - right_eye_bottom)

        blink_threshold = 0.015

        if left_eye_gap < blink_threshold and right_eye_gap < blink_threshold:
            return "Blink Detected"
        else:
            return None
    except Exception as e:
        print(f"[BlinkDetector] Error: {e}")
        return None
