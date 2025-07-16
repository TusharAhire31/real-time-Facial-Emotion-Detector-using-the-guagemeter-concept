def classify_expression(landmarks, shape):
    try:
        height, width, _ = shape
        def dist(a, b): return abs(landmarks.landmark[a].y - landmarks.landmark[b].y)

        mouth = dist(13, 14)
        left_eye = dist(159, 145)
        right_eye = dist(386, 374)
        eye_gap = (left_eye + right_eye) / 2
        brow_diff = landmarks.landmark[105].y - landmarks.landmark[334].y

        if mouth > 0.06 and eye_gap > 0.04:
            return "Fear"
        elif mouth > 0.06:
            return "Surprise"
        elif mouth > 0.04 and brow_diff < 0:
            return "Happy"
        elif mouth < 0.015 and eye_gap < 0.015:
            return "Sad"
        elif brow_diff > 0.03:
            return "Angry"
        elif brow_diff < -0.03:
            return "Guilt"
        elif abs(brow_diff) > 0.02 and mouth < 0.02:
            return "Curious"
        elif eye_gap < 0.012 and mouth < 0.02:
            return "Thinking"
        elif mouth < 0.01 and abs(brow_diff) < 0.01:
            return "Neutral"
        else:
            return "Doubt"
    except:
        return "Neutral"
