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


## Folder Structure
```
computer_vision_integration/
│
├── frame_processor.py          # Main orchestrator for processing frames
├── face_utils.py               # Face detection, cropping, ID assignment
├── gaze_headpose.py            # Gaze direction & head pose estimation
├── metrics_logger.py           # Metrics computation & CSV writing
├── ocr_utils.py                # OCR name extraction
├── config.py                   # Configurable parameters
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/muhammederbay10/BTK-HACKATHON-2025-EduVision.git
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

## Usage
Run with a video file:
```
python frame_processor.py --video_path test-data/test_video.mp4 --output_csv output.csv
```

Run with live webcam:
```
python frame_processor.py --video_path "" --output_csv live_log.csv
```
Command-line arguments:

```--video_path```:	Path to input video file. Empty string ("") for webcam.
```--output_csv```:	Path to output CSV log file.

## Output
Each run produces a CSV log with columns such as:
---
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

Additionally, cropped student face images are saved in ```photo_id/```, and name-to-ID mappings in ```photo_id/id_name_mapping.json```.

## Backend Integration

The backend server can periodically parse the CSV to collect real-time attention metrics, cross-reference IDs/photos with the JSON mapping, and use aggregate scores to issue reports or alerts. This design allows seamless integration into other educational, analytical, or monitoring platforms

## Notes

- **Performance:** EasyOCR is CPU-intensive. To accelerate, enable GPU mode in ```ocr_photo.py``` by setting ```gpu=True``` if your hardware supports it.
- **Scaling:** The system can track up to 15 faces in real time with default MediaPipe settings (adjustable in face_utils.py).
- **Lighting:** Head pose estimation is most reliable in well-lit scenes.

## Troubleshooting
If you encounter any issues:
- Double-check all dependencies are installed (```requirements.txt```)
- Confirm you are using Python 3.11 or .10 for mediapipe support
- For problems, please open an issue in the repository and include clear reproduction steps, the exact error message, and a brief environment description.
