from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import uuid
import time
from typing import Dict, List
import os
from datetime import datetime

app = FastAPI(title="Attention Tracking API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data storage
mock_reports = {}

def load_mock_data():
    """Load mock report data"""
    try:
        with open("app/data/mock_reports.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_mock_data(data):
    """Save mock report data"""
    os.makedirs("app/data", exist_ok=True)
    with open("app/data/mock_reports.json", "w") as f:
        json.dump(data, f, indent=2)

@app.get("/")
async def root():
    return {"message": "Attention Tracking API is running"}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Simulate video upload and return report ID"""
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Generate unique report ID
    report_id = str(uuid.uuid4())
    
    # Create mock report entry
    mock_reports[report_id] = {
        "id": report_id,
        "filename": file.filename,
        "upload_time": datetime.now().isoformat(),
        "status": "processing",
        "file_size": file.size if hasattr(file, 'size') else 1024000
    }
    
    save_mock_data(mock_reports)
    
    return {
        "report_id": report_id,
        "status": "uploaded",
        "message": "Video uploaded successfully"
    }

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get detailed report data"""
    
    # Load mock data
    mock_data = load_mock_data()
    
    if report_id not in mock_data and report_id not in mock_reports:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Return comprehensive mock report
    return {
        "id": report_id,
        "filename": f"lesson_video_{report_id[:8]}.mp4",
        "upload_time": datetime.now().isoformat(),
        "duration": "15:30",
        "total_students": 24,
        "average_attention": 0.73,
        "engagement_trends": [
            {"timestamp": "00:01:00", "score": 0.78, "students_engaged": 19},
            {"timestamp": "00:02:00", "score": 0.63, "students_engaged": 15},
            {"timestamp": "00:03:00", "score": 0.82, "students_engaged": 20},
            {"timestamp": "00:04:00", "score": 0.71, "students_engaged": 17},
            {"timestamp": "00:05:00", "score": 0.89, "students_engaged": 21},
            {"timestamp": "00:06:00", "score": 0.67, "students_engaged": 16},
            {"timestamp": "00:07:00", "score": 0.45, "students_engaged": 11},
            {"timestamp": "00:08:00", "score": 0.39, "students_engaged": 9},
            {"timestamp": "00:09:00", "score": 0.56, "students_engaged": 13},
            {"timestamp": "00:10:00", "score": 0.74, "students_engaged": 18},
            {"timestamp": "00:11:00", "score": 0.81, "students_engaged": 19},
            {"timestamp": "00:12:00", "score": 0.69, "students_engaged": 17},
            {"timestamp": "00:13:00", "score": 0.42, "students_engaged": 10},
            {"timestamp": "00:14:00", "score": 0.21, "students_engaged": 5},
            {"timestamp": "00:15:00", "score": 0.65, "students_engaged": 16}
        ],
        "high_engagement": {
            "timestamp": "00:05:00",
            "summary": "Teacher demonstrated interactive problem-solving with student participation",
            "score": 0.89,
            "duration": "2:15"
        },
        "low_engagement": {
            "timestamp": "00:14:00",
            "summary": "Teacher was reading definitions from slides with minimal interaction",
            "score": 0.21,
            "duration": "1:45"
        },
        "insights": {
            "most_engaging_topics": [
                "Interactive problem solving",
                "Q&A sessions",
                "Visual demonstrations"
            ],
            "least_engaging_topics": [
                "Theory reading",
                "Definition explanations",
                "Administrative announcements"
            ],
            "recommendations": [
                "Incorporate more interactive elements during theory sections",
                "Use visual aids and examples when introducing new concepts",
                "Break up long explanations with student questions",
                "Consider shorter segments for complex topics"
            ]
        },
        "llm_feedback": "Your lesson shows strong peaks during interactive moments. Consider breaking up theory-heavy sections with more frequent student engagement opportunities. The problem-solving segment at 5:00 was particularly effective - similar interactive approaches could boost attention during lower-engagement periods."
    }

@app.get("/api/reports")
async def get_all_reports():
    """Get list of all reports"""
    mock_data = load_mock_data()
    
    # Combine stored and current session reports
    all_reports = {**mock_data, **mock_reports}
    
    # Add some default mock reports if none exist
    if not all_reports:
        default_reports = {
            "demo-1": {
                "id": "demo-1",
                "filename": "math_lesson_intro.mp4",
                "upload_time": "2024-01-15T10:30:00",
                "average_attention": 0.76,
                "duration": "12:45"
            },
            "demo-2": {
                "id": "demo-2", 
                "filename": "physics_experiment.mp4",
                "upload_time": "2024-01-14T14:20:00",
                "average_attention": 0.82,
                "duration": "18:20"
            },
            "demo-3": {
                "id": "demo-3",
                "filename": "history_discussion.mp4", 
                "upload_time": "2024-01-12T09:15:00",
                "average_attention": 0.68,
                "duration": "25:10"
            }
        }
        all_reports = default_reports
        save_mock_data(all_reports)
    
    return {"reports": list(all_reports.values())}

@app.get("/api/processing/{report_id}")
async def get_processing_status(report_id: str):
    """Get processing status for a report"""
    
    # Simulate processing stages
    stages = [
        {"stage": "analyzing_faces", "progress": 20, "message": "Analyzing faces and expressions..."},
        {"stage": "extracting_attention", "progress": 60, "message": "Extracting attention patterns..."},
        {"stage": "generating_feedback", "progress": 90, "message": "Generating insights and feedback..."},
        {"stage": "complete", "progress": 100, "message": "Analysis complete!"}
    ]
    
    # For demo, return different stages based on timing
    import time
    current_time = int(time.time()) % 20
    
    if current_time < 5:
        return stages[0]
    elif current_time < 12:
        return stages[1]
    elif current_time < 18:
        return stages[2]
    else:
        return stages[3]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)