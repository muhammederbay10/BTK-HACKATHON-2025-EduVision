import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import time
import uuid
import argparse
from datetime import datetime
import sys
import traceback
import os
import json
import easyocr

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=15,
    refine_landmarks=False,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# Drawing utilities 
mp_drawing = mp.solutions.drawing_utils
draw_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS = [468]
RIGHT_IRIS = [473]



# CSV Output Setup
def setup_csv_output(csv_file_path=None):
    """
    Sets up the CSV logging file. Resumes from existing file or creates a new one.

    Args:
        csv_file_path (str): Optional custom path for the CSV file.

    Returns:
        Tuple: (csv_file_path, FIELDNAMES list, starting frame index)
    """
    if csv_file_path is None:
        csv_file_path = "student_attention_log.csv"
    
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
        df = pd.read_csv(csv_file_path)
        frame_idx = len(df)
    except FileNotFoundError:
        df = pd.DataFrame(columns=FIELDNAMES)
        frame_idx = 0
    
    return csv_file_path, FIELDNAMES, frame_idx
<<<<<<< HEAD

# Handle output path
def handle_output_path(output_path):
    """Ensure output path has the correct extension (.csv)"""
    if not output_path:
        return None
        
    # Make sure the output path has a .csv extension
    if not output_path.lower().endswith('.csv'):
        # Change the extension to .csv
        base_path = os.path.splitext(output_path)[0]
        output_path = base_path + '.csv'
        print(f"Changed output path to: {output_path}")
    
    # Make sure the directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    return output_path
=======
>>>>>>> 5823334 (Add CLI support, refactor CSV logic, and improve error handling)



# Student IDs (assign face ids)
student_ids = {}

def assign_student_id(face_landmarks, student_ids, frame_w, frame_h):
    """
    Assigns or re-identifies a student ID based on face position.

    Args:
        face_landmarks: Face landmarks detected by Mediapipe.
        student_ids (dict): Dictionary of known IDs and their last positions.
        frame_w (int): Frame width.
        frame_h (int): Frame height.

    Returns:
        str: Assigned student ID.
    """
    # Use the nose tip + left/right eye position to assign/reidentify students
    key_points = [face_landmarks.landmark[i] for i in [1, 33, 263]]
    nose_tip = (int(key_points[0].x*frame_w), int(key_points[0].y*frame_h))
    min_dist = float('inf')
    min_id = None
    for s_id, last_pos in student_ids.items():
        d = np.linalg.norm(np.array(nose_tip) - np.array(last_pos))
        if d < 50:   # If in a reasonable distance, consider as the same student (tweak as needed)
            if d < min_dist:
                min_dist = d
                min_id = s_id
    if min_id is not None:
        student_ids[min_id] = nose_tip
        return min_id, False   # NOT a new student
    # If new face, assign new ID
    new_id = str(uuid.uuid4())[:8]
    student_ids[new_id] = nose_tip
    return new_id, True        # NEW student



def ensure_photo_dir_exists(photo_dir="photo_id"):
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)
    return photo_dir



def save_face_photo(frame, face_landmarks, frame_w, frame_h, student_id, photo_dir="photo_id"):
    # Extract all landmark points as pixel coords
    points = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in face_landmarks.landmark]
    x_vals, y_vals = zip(*points)
    # Proportional padding
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    box_w = max_x - min_x
    box_h = max_y - min_y
    # Individual side paddings (customize these ratios as needed)
    pad_left_ratio = 1.3
    pad_right_ratio = 0.2
    pad_top_ratio = 0.3
    pad_bottom_ratio = 0.4
    pad_left = int(box_w * pad_left_ratio)
    pad_right = int(box_w * pad_right_ratio)
    pad_top = int(box_h * pad_top_ratio)
    pad_bottom = int(box_h * pad_bottom_ratio)
    x1 = max(min_x - pad_left, 0)
    y1 = max(min_y - pad_top, 0)
    x2 = min(max_x + pad_right, frame_w-1)
    y2 = min(max_y + pad_bottom, frame_h-1)
    face_img = frame[y1:y2, x1:x2]
    out_path = os.path.join(photo_dir, f"{student_id}.jpg")
    cv2.imwrite(out_path, face_img)



def crop_face_with_padding(frame, face_landmarks, frame_w, frame_h, 
                          pad_left_ratio=0.2, pad_right_ratio=0.2,
                          pad_top_ratio=0.3, pad_bottom_ratio=0.4):
    points = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in face_landmarks.landmark]
    x_vals, y_vals = zip(*points)
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    box_w = max_x - min_x
    box_h = max_y - min_y
    pad_left = int(box_w * pad_left_ratio)
    pad_right = int(box_w * pad_right_ratio)
    pad_top = int(box_h * pad_top_ratio)
    pad_bottom = int(box_h * pad_bottom_ratio)
    x1 = max(min_x - pad_left, 0)
    y1 = max(min_y - pad_top, 0)
    x2 = min(max_x + pad_right, frame_w-1)
    y2 = min(max_y + pad_bottom, frame_h-1)
    return frame[y1:y2, x1:x2]



def extract_name_easyocr_from_array(img_array, show_debug=False):
    reader = easyocr.Reader(['en'], gpu=False)
    h, w = img_array.shape[:2]
    scale = 4
    image_up = cv2.resize(img_array, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
    h_up, w_up = image_up.shape[:2]
    crop_top = int(h_up * 0.60)
    crop_left = 0
    crop_bottom = h_up
    crop_right = int(w_up * 0.80)
    cropped = image_up[crop_top:crop_bottom, crop_left:crop_right]
    results = reader.readtext(cropped)
    if show_debug:
        for (bbox, text, confidence) in results:
            print(f"[{confidence:.2f}] {text}")
        cv2.imwrite("debug_output.jpg", cropped)
        print("Saved debug image as debug_output.jpg")
    if results:
        results.sort(key=lambda r: r[0][0][0])
        return " ".join([r[1] for r in results])
    else:
        return "Name not found"



def get_gaze_direction(iris, eye_corners):
    """
    Estimates gaze direction by comparing iris position relative to the eye.

    Args:
        iris (list): Coordinates of the iris center.
        eye_corners (list): Coordinates of the eye corners.

    Returns:
        str: One of 'Left', 'Center', 'Right', or 'unknown'.
    """
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
    """
    Estimates the head's rotation vector (3D orientation) using selected landmarks.

    Args:
        landmarks (dict): Dictionary of facial landmarks.
        frame_w (int): Frame width.
        frame_h (int): Frame height.

    Returns:
        np.ndarray: Rotation vector (3D angle representation).
    """
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
    """
    Determines attention status based on gaze direction and yaw angle.

    Args:
        gaze (str): Estimated gaze direction.
        rotation_vector (np.ndarray): Head pose rotation vector.

    Returns:
        Tuple[str, float]: Attention status ('Attentive' or 'Not attentive') and yaw angle in degrees.
    """
    yaw = rotation_vector[1][0] * (180.0 / np.pi)
    if abs(yaw) > 25 or gaze in ["Left", "Right"]:
        return "Not attentive", yaw
    else:
        return "Attentive", yaw



# Per student statistics (reinit each session)
student_data = {}

def update_student_metrics(student_id, attention, timestamp):
    """
    Updates a student's attention statistics for the current frame.

    Args:
        student_id (str): Unique student identifier.
        attention (str): Attention status ('Attentive' or 'Not attentive').
        timestamp (float): Current time.

    Returns:
        dict: Updated metrics for the student.
    """
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

    # (yawning count and eye closure can be implemented later)
    # Placeholder: focus quality etc
    return data



def compute_metrics(data):
    """
    Computes overall session statistics for a student.

    Args:
        data (dict): Student's attention metrics.

    Returns:
        Tuple[float, int, int, float, float, float]: Attention score, events, yawns, closures, duration, rate.
    """
    attention_score = (data["attentive_frames"] / data["total_frames"])*100 if data["total_frames"] > 0 else 0
    session_duration = (data["last_frame_time"] - data["first_frame_time"])/60
    distraction_rate = data["distraction_events"] / session_duration if session_duration > 0 else 0
    return attention_score, data["distraction_events"], data["yawning_count"], data["eye_closure_duration_sec"], session_duration, distraction_rate



def handle_new_student(frame, face_landmarks, frame_w, frame_h, student_id, mapping_json_path, photo_dir="photo_ID"):
    # Wide crop (for name extraction)
    wide_img = crop_face_with_padding(
        frame, face_landmarks, frame_w, frame_h,
        pad_left_ratio=1.3, pad_right_ratio=0.2,
        pad_top_ratio=0.3, pad_bottom_ratio=0.4
    )
    # Extract name using OCR (note: works directly on numpy array)
    name = extract_name_easyocr_from_array(wide_img, show_debug=False)
    print(f"OCR got name: {name}")

    # Update ID-name mapping JSON
    if os.path.exists(mapping_json_path):
        with open(mapping_json_path, 'r') as f:
            mapping = json.load(f)
    else:
        mapping = {}
    mapping[student_id] = name
    with open(mapping_json_path, 'w') as f:
        json.dump(mapping, f, indent=2)

    # Regular crop for photo_ID directory
    normal_img = crop_face_with_padding(
        frame, face_landmarks, frame_w, frame_h,
        pad_left_ratio=0.30, pad_right_ratio=0.30,
        pad_top_ratio=0.50, pad_bottom_ratio=0.50
    )
    os.makedirs(photo_dir, exist_ok=True)
    normal_img_path = os.path.join(photo_dir, f"{student_id}.jpg")
    cv2.imwrite(normal_img_path, normal_img)



def main():
    photo_dir = ensure_photo_dir_exists()
    parser = argparse.ArgumentParser(description='Attention Tracker')
    parser.add_argument('--video_path', type=str, default='test-data/test_video.mp4', help='Path to input video file (default: webcam)')
    parser.add_argument('--output_csv', type=str, default='student_attention_log.csv', help='Output CSV file path')
    
    args = parser.parse_args()
    
    # Setup CSV output
    csv_file_path, fieldnames, frame_idx = setup_csv_output(args.output_csv)
<<<<<<< HEAD
    csv_file_path = handle_output_path(csv_file_path)
=======
>>>>>>> 5823334 (Add CLI support, refactor CSV logic, and improve error handling)
    
    # Setup video capture
    if args.video_path:
        cap = cv2.VideoCapture(args.video_path)
        print(f"Processing video: {args.video_path}")
    else:
        cap = cv2.VideoCapture(0)
        print("Running live webcam... Press 'q' to quit.")

    if not cap.isOpened():
        print("Error: Could not open video source", file=sys.stderr)
        sys.exit(1)

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Failed to grab frame or reached end of video.")
                break
                
            if not args.video_path:  # Only flip for webcam
                frame = cv2.flip(frame, 1)
                
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            now = time.time()
            timestamp = datetime.now().isoformat()
            
            # Every frame's data will be appended to CSV using pandas
            row_data = []
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # Assign ID & store photo ID for new student IDs
                    s_id, is_new = assign_student_id(face_landmarks, student_ids, w, h)
                    if is_new:
                        handle_new_student(
                            frame, face_landmarks, w, h, s_id,
                            mapping_json_path="photo_id/id_name_mapping.json", photo_dir=photo_dir
                        )
                    # Landmarks extraction
                    landmarks = {}
                    for i, lm in enumerate(face_landmarks.landmark):
                        x, y = int(lm.x * w), int(lm.y * h)
                        landmarks[i] = (x, y)
                    # Gaze
                    if all(i in landmarks for i in LEFT_IRIS + LEFT_EYE):
                        left_iris = [landmarks[i] for i in LEFT_IRIS]
                        left_eye = [landmarks[i] for i in LEFT_EYE]
                        gaze = get_gaze_direction(left_iris, left_eye)
                    else:
                        gaze = "unknown"
                    # Head pose
                    try:
                        rot_vec = estimate_head_pose(landmarks, w, h)
                    except:
                        continue  # Skip if can't estimate
                    attention, yaw_angle = get_attention_label(gaze, rot_vec)
                    # Update student data
                    metrics = update_student_metrics(s_id, attention, now)
                    # CSV metrics
                    a_score, distraction_events, yawning_count, closure_dur, session_duration, distraction_rate = compute_metrics(metrics)
                    # Placeholder for focus quality
                    focus_quality = ""
                    # Append to per-frame record
                    row_data.append({
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
                        "focus_quality": focus_quality,
                        "session_duration_minutes": round(session_duration,2)
                    })
                    # Drawings
                    x, y = landmarks[1]
                    cv2.putText(frame, f"ID:{s_id[:4]}", (x-30, y-45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,128,255), 1)
                    cv2.putText(frame, f"Gaze:{gaze}", (x-30, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                    cv2.putText(frame, f"Status:{attention}", (x-30, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255) if attention=="Not attentive" else (0,255,0), 1)
                    cv2.circle(frame, (x, y), 3, (255,0,0), -1)
            
            # Per-frame CSV write to make it robust to interruption
            if row_data:
                new_df = pd.DataFrame(row_data)
                new_df.to_csv(csv_file_path, index=False, mode='a', header=not bool(frame_idx))
                frame_idx += 1
            
            # Show window only for webcam mode
            if not args.video_path:
                cv2.imshow('Multi-Person Attention Tracker', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except Exception as e:
        print(f"\n--- An error occurred in attention_tracker.py ---", file=sys.stderr)
        print(f"ERROR: {e}", file=sys.stderr)
        print("\n--- Traceback ---", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


    cap.release()
    cv2.destroyAllWindows()
    print(f"Analysis complete. Results saved to: {csv_file_path}")

if __name__ == "__main__":
    main()