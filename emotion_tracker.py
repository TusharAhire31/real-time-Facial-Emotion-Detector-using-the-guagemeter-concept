from collections import deque, Counter

class EmotionTracker:
    def __init__(self, max_len=100):
        self.recent_emotions = deque(maxlen=max_len)

    def update(self, emotion):
        self.recent_emotions.append(emotion)

    def get_emotion_counts(self):
        return dict(Counter(self.recent_emotions))
