# frame_processor.py
import time
import json
import os
import cv2
import pandas as pd

from face_utils import create_face_mesh, landmarks_to_dict, get_gaze_direction, estimate_head_pose, get_attention_label, draw_annotations, LEFT_EYE, LEFT_IRIS
from id_manager import assign_student_id, student_ids
from ocr_photo import ensure_photo_dir_exists, handle_new_student
from metrics import update_student_metrics, compute_metrics
from csv_logger import setup_csv_output, append_rows

def initialize_tracking(video_path, output_csv):
    """
    Prepare capture, mapping JSON, CSV and MediaPipe face mesh.
    Returns: cap, face_mesh, mapping_json_path, id_name_mapping, csv_file_path, frame_idx, photo_dir
    """
    photo_dir = ensure_photo_dir_exists()
    mapping_json_path = os.path.join("photo_id", "id_name_mapping.json")
    if os.path.exists(mapping_json_path):
        with open(mapping_json_path, 'r') as f:
            id_name_mapping = json.load(f)
    else:
        id_name_mapping = {}

    csv_file_path, fieldnames, frame_idx = setup_csv_output(output_csv)

    if video_path:
        cap = cv2.VideoCapture(video_path)
    else:
        cap = cv2.VideoCapture(0)

    face_mesh = create_face_mesh()
    return cap, face_mesh, mapping_json_path, id_name_mapping, csv_file_path, frame_idx, photo_dir

def process_frame(frame, face_mesh, mapping_json_path, id_name_mapping, csv_file_path, frame_idx):
    """
    Processes one frame: detects faces, assigns IDs, runs OCR on new faces, computes metrics,
    writes CSV rows, and draws annotations on the frame.
    Returns: updated frame_idx and id_name_mapping
    """
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    now = time.time()
    timestamp = pd.Timestamp.now().isoformat()
    row_data = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            s_id, is_new = assign_student_id(face_landmarks, student_ids, w, h)
            if is_new:
                handle_new_student(frame, face_landmarks, w, h, s_id, mapping_json_path=mapping_json_path, photo_dir="photo_id")
                # refresh mapping
                if os.path.exists(mapping_json_path):
                    with open(mapping_json_path, 'r') as f:
                        id_name_mapping = json.load(f)

            landmarks = landmarks_to_dict(face_landmarks, w, h)

            # gaze using left eye (same as original)
            if all(i in landmarks for i in LEFT_IRIS + LEFT_EYE):
                left_iris = [landmarks[i] for i in LEFT_IRIS]
                left_eye = [landmarks[i] for i in LEFT_EYE]
                gaze = get_gaze_direction(left_iris, left_eye)
            else:
                gaze = "unknown"

            try:
                rot_vec = estimate_head_pose(landmarks, w, h)
            except Exception:
                continue

            attention, yaw_angle = get_attention_label(gaze, rot_vec)
            metrics = update_student_metrics(s_id, attention, now)
            a_score, distraction_events, yawning_count, closure_dur, session_duration, distraction_rate = compute_metrics(metrics)

            student_name = id_name_mapping.get(s_id, "Unknown")

            row_data.append({
                "student_name": student_name,
                "student_id": s_id,
                "timestamp": timestamp,
                "frame_idx": frame_idx,
                "attention_status": attention,
                "gaze": gaze,
                "yaw_angle_deg": yaw_angle,
                "attention_score": round(a_score,1),
                "distraction_events": distraction_events,
                "yawning_count": yawning_count,
                "eye_closure_duration_sec": closure_dur,
                "focus_quality": "",
                "session_duration_minutes": round(session_duration,2)
            })

            draw_annotations(frame, landmarks, s_id, gaze, attention)

    if row_data:
        new_df = pd.DataFrame(row_data)
        append_rows(csv_file_path, new_df, frame_idx)
        frame_idx += 1

    return frame, frame_idx, id_name_mapping
