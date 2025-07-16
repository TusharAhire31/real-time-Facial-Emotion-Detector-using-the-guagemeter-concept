# File: gui_main.py
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
from datetime import datetime
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from utils.expression_classifier import classify_expression
from utils.blink_detector import detect_blinks
from utils.emotion_tracker import EmotionTracker
from utils.csv_logger import log_emotion

# Emotion setup
EMOTIONS = ["Happy", "Sad", "Angry", "Fear", "Surprise", "Guilt", "Doubt", "Thinking", "Curious", "Neutral"]
colors = {
    "Happy": "lime",
    "Sad": "cyan",
    "Angry": "red",
    "Fear": "magenta",
    "Surprise": "yellow",
    "Guilt": "orange",
    "Doubt": "blue",
    "Thinking": "white",
    "Curious": "pink",
    "Neutral": "gray"
}

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.6)
cap = cv2.VideoCapture(0)
emotion_tracker = EmotionTracker()

root = tk.Tk()
root.title("Emotion Detection - Gauge UI")
root.configure(bg='black')

video_label = tk.Label(root)
video_label.grid(row=0, column=0)

fig, axs = plt.subplots(2, 5, figsize=(9, 4), facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1)

for ax in axs.flatten():
    ax.set_facecolor("black")
    ax.axis('off')

def draw_gauges():
    history = emotion_tracker.get_emotion_counts()
    for i, emotion in enumerate(EMOTIONS):
        row, col = divmod(i, 5)
        ax = axs[row][col]
        ax.clear()
        ax.set_facecolor("black")
        val = history.get(emotion, 0) % 10
        theta = np.linspace(0, np.pi, 100)
        ax.plot(np.cos(theta), np.sin(theta), color='white', lw=2)
        ax.plot([0, np.cos(np.pi * val / 10)], [0, np.sin(np.pi * val / 10)], color=colors[emotion], lw=3)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(0, 1.2)
        ax.set_title(emotion, color=colors[emotion], fontsize=9)
        ax.axis('off')
    canvas.draw()

def draw_face_circle(frame, landmarks):
    h, w, _ = frame.shape
    xs = [int(p.x * w) for p in landmarks.landmark]
    ys = [int(p.y * h) for p in landmarks.landmark]
    center_x, center_y = int(np.mean(xs)), int(np.mean(ys))
    radius = int(max(np.std(xs), np.std(ys)) * 3)
    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 255), 1)

def update_frame():
    success, frame = cap.read()
    if not success:
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)
    expression = "Neutral"

    if result.multi_face_landmarks:
        for landmarks in result.multi_face_landmarks:
            draw_face_circle(frame, landmarks)
            expression = classify_expression(landmarks, frame.shape)
            emotion_tracker.update(expression)
            log_emotion(expression)
            break

    draw_gauges()
    cv2.putText(frame, f"Detected: {expression}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    video_label.after(100, update_frame)

update_frame()
root.mainloop()
cap.release()
cv2.destroyAllWindows()
