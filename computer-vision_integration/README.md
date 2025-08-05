# Computer Vision Module — Student Attention Tracking

This module is part of a larger project that analyzes student attention during online or recorded lessons. It uses **computer vision** techniques to track facial features in real time and logs attention-related metrics, which are later used by an NLP pipeline to generate actionable lesson reports for teachers.

---

## Overview

This module:
- Detects multiple faces in a video stream (live or pre-recorded)
- Identifies gaze direction (left, center, right)
- Estimates head pose to determine yaw angle
- Tracks per-student attention status over time
- Logs data per frame to a CSV file (`student_attention_log.csv`)

The recorded metrics are used downstream by an **NLP module** to automatically generate lesson summaries and insights.

---

## How It Works

For each detected face:
1. **Assigns a temporary unique student ID** based on nose & eye position tracking
2. **Tracks gaze direction** using iris position relative to the eye corners
3. **Estimates head yaw angle** using a 3D model of the face
4. **Classifies attention** as:
   - **Attentive**: Gaze centered, head facing forward
   - **Not attentive**: Head turned or eyes looking away
5. **Updates attention statistics** over the session

All frame-level data is appended to a CSV file for robustness.

---

## Output: `student_attention_log.csv`

| Column Name               | Description                                              |
|---------------------------|----------------------------------------------------------|
| `student_id`              | Unique ID per face                                       |
| `timestamp`               | ISO-formatted timestamp                                  |
| `frame_idx`               | Frame number                                             |
| `attention_status`        | Attentive / Not attentive                                |
| `gaze`                    | Left / Center / Right / Unknown                          |
| `yaw_angle_deg`           | Head yaw angle in degrees                                |
| `attention_score`         | % of time attentive (up to this frame)                   |
| `distraction_events`      | Number of attention loss events                          |
| `yawning_count`           | (Placeholder) — to be implemented                        |
| `eye_closure_duration_sec`| (Placeholder) — to be implemented                        |
| `focus_quality`           | (Placeholder for future focus score)                     |
| `session_duration_minutes`| Duration since student's first frame                     |

---

## Running the Module

