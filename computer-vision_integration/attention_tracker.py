import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import uuid
from datetime import datetime

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=5,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Drawing utilities (optional)
mp_drawing = mp.solutions.drawing_utils
draw_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS = [468]
RIGHT_IRIS = [473]

# CSV Output Setup
CSV_FILE = "student_attention_log.csv"
FIELDNAMES = [
    "student_id", 
    "timestamp", 
    "frame_idx", 
    "attention_status", 
    "gaze", 
    "yaw_angle_deg", 
    "attention_score", 
    "distraction_events", 
    "yawning_count", 
    "eye_closure_duration_sec", 
    "focus_quality", 
    "session_duration_minutes"
]

# Start/Resume CSV
try:
    df = pd.read_csv(CSV_FILE)
    frame_idx = len(df)
except FileNotFoundError:
    df = pd.DataFrame(columns=FIELDNAMES)
    frame_idx = 0

# Student IDs (assign face ids)
student_ids = {}
