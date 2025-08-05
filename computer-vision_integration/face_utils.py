# face_utils.py
import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Indices used in original script
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS = [468]
RIGHT_IRIS = [473]

def create_face_mesh(max_num_faces=15, refine_landmarks=False, 
                     min_detection_confidence=0.3, min_tracking_confidence=0.3):
    return mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=max_num_faces,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence
    )

def landmarks_to_dict(face_landmarks, frame_w, frame_h):
    landmarks = {}
    for i, lm in enumerate(face_landmarks.landmark):
        x, y = int(lm.x * frame_w), int(lm.y * frame_h)
        landmarks[i] = (x, y)
    return landmarks

def get_gaze_direction(iris, eye_corners):
    # same logic as original
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
    # copies original PnP mapping - returns rotation_vector
    image_points = np.array([
        (landmarks[1][0], landmarks[1][1]),    # Nose tip
        (landmarks[152][0], landmarks[152][1]),# Chin
        (landmarks[263][0], landmarks[263][1]),# Left eye right corner
        (landmarks[33][0], landmarks[33][1]),  # Right eye left corner
        (landmarks[287][0], landmarks[287][1]),# Left mouth corner
        (landmarks[57][0], landmarks[57][1])   # Right mouth corner
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

def draw_annotations(frame, landmarks, s_id, gaze, attention):
    # Draws the same overlays (small text + dot) as original
    x, y = landmarks[1]
    cv2.putText(frame, f"ID:{s_id[:4]}", (x-30, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,255), 1)
    cv2.putText(frame, f"Gaze:{gaze}", (x-30, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    color = (0,0,255) if attention=="Not attentive" else (0,255,0)
    cv2.putText(frame, f"Status:{attention}", (x-30, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    cv2.circle(frame, (x, y), 3, (255,0,0), -1)
