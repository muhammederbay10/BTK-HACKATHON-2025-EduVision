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
student_data = {}

def update_student_metrics(student_id, attention, timestamp):
    if student_id not in student_data:
        student_data[student_id] = {
            "total_frames": 0, "attentive_frames": 0, "not_attentive_frames": 0,
            "distraction_events": 0, "was_attentive": True,
            "first_frame_time": timestamp, "last_frame_time": timestamp,
            "yawning_count": 0, "eye_closure_duration_sec": 0,
        }
    data = student_data[student_id]
    data["total_frames"] += 1
    if attention == "Attentive":
        data["attentive_frames"] += 1
        data["was_attentive"] = True
    else:
        data["not_attentive_frames"] += 1
        if data["was_attentive"]:
            data["distraction_events"] += 1
        data["was_attentive"] = False
    data["last_frame_time"] = timestamp
    return data

def compute_metrics(data):
    attention_score = (data["attentive_frames"] / data["total_frames"])*100 if data["total_frames"] > 0 else 0
    session_duration = (data["last_frame_time"] - data["first_frame_time"])/60
    distraction_rate = data["distraction_events"] / session_duration if session_duration > 0 else 0
    return attention_score, data["distraction_events"], data["yawning_count"], data["eye_closure_duration_sec"], session_duration, distraction_rate



def assign_student_id(face_landmarks, student_ids, frame_w, frame_h):
    key_points = [face_landmarks.landmark[i] for i in [1, 33, 263]]
    nose_tip = (int(key_points[0].x*frame_w), int(key_points[0].y*frame_h))
    min_dist = float('inf')
    min_id = None
    for s_id, last_pos in student_ids.items():
        d = np.linalg.norm(np.array(nose_tip) - np.array(last_pos))
        if d < 50:
            if d < min_dist:
                min_dist = d
                min_id = s_id
    if min_id is not None:
        student_ids[min_id] = nose_tip
        return min_id
    new_id = str(uuid.uuid4())[:8]
    student_ids[new_id] = nose_tip
    return new_id

def get_gaze_direction(iris, eye_corners):
    eye_left = np.array(eye_corners[0])
    eye_right = np.array(eye_corners[1])
    iris = np.array(iris[0])
    eye_width = np.linalg.norm(eye_right - eye_left)
    if eye_width == 0: return "unknown"
    ratio = (iris[0] - eye_left[0]) / eye_width
    if ratio < 0.35:
        return "Right"
    elif ratio > 0.65:
        return "Left"
    else:
        return "Center"
    
def estimate_head_pose(landmarks, frame_w, frame_h):
    image_points = np.array([
        (landmarks[1][0], landmarks[1][1]),
        (landmarks[152][0], landmarks[152][1]),
        (landmarks[263][0], landmarks[263][1]),
        (landmarks[33][0], landmarks[33][1]),
        (landmarks[287][0], landmarks[287][1]),
        (landmarks[57][0], landmarks[57][1])
    ], dtype="double")
    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -63.6, -12.5),
        (-43.3, 32.7, -26.0),
        (43.3, 32.7, -26.0),
        (-28.9, -28.9, -24.1),
        (28.9, -28.9, -24.1)
    ])
    focal_length = frame_w
    center = (frame_w / 2, frame_h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")
    dist_coeffs = np.zeros((4,1))
    success, rotation_vector, translation_vector = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs)
    return rotation_vector

def get_attention_label(gaze, rotation_vector):
    yaw = rotation_vector[1][0] * (180.0 / np.pi)
    if abs(yaw) > 25 or gaze in ["Left", "Right"]:
        return "Not attentive", yaw
    else:
        return "Attentive", yaw