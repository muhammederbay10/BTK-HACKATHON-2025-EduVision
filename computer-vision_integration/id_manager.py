# id_manager.py
import uuid
import numpy as np

student_ids = {}

def assign_student_id(face_landmarks, student_ids_dict, frame_w, frame_h, distance_threshold=50):
    """
    Same logic as original assign_student_id: uses nose tip + eyes to re-id by distance.
    Returns (student_id, is_new)
    """
    key_points = [face_landmarks.landmark[i] for i in [1, 33, 263]]
    nose_tip = (int(key_points[0].x*frame_w), int(key_points[0].y*frame_h))
    min_dist = float('inf')
    min_id = None
    for s_id, last_pos in student_ids_dict.items():
        d = np.linalg.norm(np.array(nose_tip) - np.array(last_pos))
        if d < distance_threshold:
            if d < min_dist:
                min_dist = d
                min_id = s_id
    if min_id is not None:
        student_ids_dict[min_id] = nose_tip
        return min_id, False
    new_id = str(uuid.uuid4())[:8]
    student_ids_dict[new_id] = nose_tip
    return new_id, True
