# metrics.py
import time

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
