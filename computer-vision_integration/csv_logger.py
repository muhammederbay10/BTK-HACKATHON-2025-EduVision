# csv_logger.py
import pandas as pd
import os

FIELDNAMES = [
    "student_name",
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

def setup_csv_output(csv_file_path=None):
    if csv_file_path is None:
        csv_file_path = "student_attention_log.csv"
    try:
        df = pd.read_csv(csv_file_path)
        frame_idx = len(df)
    except FileNotFoundError:
        df = pd.DataFrame(columns=FIELDNAMES)
        frame_idx = 0
    return csv_file_path, FIELDNAMES, frame_idx

def append_rows(csv_file_path, rows_df, frame_idx):
    # rows_df is a pandas DataFrame
    rows_df.to_csv(csv_file_path, index=False, mode='a', header=not bool(frame_idx))
