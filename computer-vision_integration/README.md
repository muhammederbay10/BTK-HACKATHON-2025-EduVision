# Computer Vision Integration

## Overview
This module implements **multi-person real-time attention monitoring** using:
- **MediaPipe** for face mesh detection  
- **EasyOCR** for reading student names from ID cards/badges  
- **OpenCV** for image processing & head pose estimation  
- **Custom logic** for gaze detection, attention scoring, and session metrics logging  

The system:
1. Detects faces in frames (video file or webcam)  
2. Assigns a unique **Student ID** per person  
3. Reads the **student name** using OCR (first appearance only)  
4. Tracks **gaze direction** & **head orientation**  
5. Determines **attentive / not attentive** status  
6. Logs all results into a **CSV file** for backend processing  

---

## Folder Structure
```
computer_vision_integration/
│
├── frame_processor.py # Main orchestrator for processing frames
├── face_utils.py # Face detection, cropping, ID assignment
├── gaze_headpose.py # Gaze direction & head pose estimation
├── metrics_logger.py # Metrics computation & CSV writing
├── ocr_utils.py # OCR name extraction
├── config.py # Configurable parameters
├── requirements.txt # Python dependencies
└── README.md # This file
```

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd computer_vision_integration
```
**2. Create a virtual environment & activate it**
```
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```
**3. Install dependencies**
```
pip install -r requirements.txt
```

Usage
Run with a video file:
```
python frame_processor.py --video_path test-data/test_video.mp4 --output_csv output.csv
```

Run with live webcam:
```
python frame_processor.py --video_path "" --output_csv live_log.csv
```
Arguments:

Argument	Description
--video_path	Path to input video file. Empty string ("") for webcam.
--output_csv	Path to output CSV log file.

Output
CSV file with the following columns:
```
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
```
Face images saved in photo_id/ for each student
Name-ID mapping in photo_id/id_name_mapping.json

## Backend Integration
The backend can:

Periodically read the generated CSV for real-time metrics

Map student IDs to photos using the JSON mapping

Use the attention scores to generate reports or trigger alerts

## Notes
EasyOCR is CPU-heavy; enable GPU by setting gpu=True in ocr_utils.py if available.

Mediapipe face mesh runs in real-time for up to 15 faces, but increase max_num_faces in config.py if needed.

Head pose estimation uses a simple PnP model — works best with good lighting.

## Future Improvements
Add yawning & eye closure detection

Integrate with an actual object tracker (e.g., SORT, DeepSORT) for even more robust ID assignment

Stream results via WebSocket to backend in real-time

## Module Explanations
frame_processor.py
The main entry point of the module.

Reads frames from a video file or webcam

Calls face_utils to detect & crop faces

Calls ocr_utils to read student names (first-time detection)

Calls gaze_headpose to estimate gaze direction & head orientation

Updates attention metrics & sends them to metrics_logger

Saves processed images & logs results

face_utils.py
Handles:

Face detection using MediaPipe FaceMesh

Cropping face regions for further analysis

Assigning Student IDs to maintain identity across frames

Handling multiple faces in real time

gaze_headpose.py
Responsible for:

Gaze detection (looking left, right, forward, down)

Head pose estimation (yaw, pitch, roll angles)

Classifying if a person is attentive or not attentive

Works in sync with face_utils to ensure correct face mapping

metrics_logger.py
Handles:

Writing all attention metrics to CSV

Tracking:

Distraction events

Yawning count

Eye closure duration

Attention score per student

Session duration & focus quality

ocr_utils.py
Extracts student names from ID cards, badges, or name tags

Uses EasyOCR with custom preprocessing to improve recognition

Stores mapping between student_id and student_name in a JSON file

config.py
Holds all tweakable parameters:

Face mesh settings

OCR parameters

Gaze & head pose thresholds

Maximum allowed faces

Paths for saving data

## Error Handling
If you encounter any issues:

Check the requirements.txt for missing dependencies

Make sure your Python version is >= 3.8

Create an issue in the repository with:

Steps to reproduce

Error message

Environment details
