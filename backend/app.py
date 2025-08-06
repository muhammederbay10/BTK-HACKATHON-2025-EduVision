import os
import uuid
import threading
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import RedirectResponse # type: ignore

# Import video processor module
from .video_processor import process_video_task, get_status, SUPPORTED_LANGUAGES

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set absolute paths for all directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create logs and reports directories required by NLP script
project_root = os.path.dirname(BASE_DIR)
os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
os.makedirs(os.path.join(project_root, "reports"), exist_ok=True)
# Create reports directory in the backend folder too
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

@app.post("/api/upload")
async def upload_video(
    file: UploadFile = File(...), 
    lessonName: str = Form("default_lesson"), 
    language: str = Form("english")
):

    print("======= FORM DATA RECEIVED =======")
    print(f"Lesson Name: '{lessonName}'")
    print(f"Language: '{language}'")
    print(f"File name: '{file.filename}'")
    print("=================================")
    video_id = str(uuid.uuid4())
    print(f"Generated video_id: {video_id} for course '{lessonName}'")
    video_path = os.path.join(UPLOAD_DIR, f"{video_id}.mp4")
    print(f"Video path: {video_path}")

    # Save the uploaded file
    try:
        with open(video_path, "wb") as buffer:
            buffer.write(await file.read())
        print(f"Video saved to {video_path}")
    except FileNotFoundError:
        # If there's still an issue with the path, create the directory again
        print(f"Error: Directory not found. Creating directory: {UPLOAD_DIR}")
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        # Try again after ensuring directory exists
        with open(video_path, "wb") as buffer:
            buffer.write(await file.read())
    print(f"Video saved to {video_path}")
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_video_task, 
        args=(video_id, video_path, UPLOAD_DIR, lessonName, language)
    )
    thread.daemon = True
    thread.start()
    
    # Return immediately with the video ID
    return {"reportId": video_id}


@app.get("/api/status/{report_id}")
async def get_processing_status(report_id: str):
    """Check the processing status of a video"""
    print(f"Checking status for report_id: {report_id}")
    
    status = get_status(report_id)
    return {"status": status}

@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    """Get the processing report for a video"""
    print(f"Getting report for report_id: {report_id}")
    
    # First, check if processing is still ongoing
    status = get_status(report_id)
    if status == "processing":
        return {"status": "processing", "message": "Report is still being generated"}
    
    # First try to find the report in the backend reports directory
    backend_reports_dir = os.path.join(BASE_DIR, "reports")
    backend_report_path = os.path.join(backend_reports_dir, f"{report_id}.json")
    
    # If not in backend reports dir, look in upload directory as fallback
    report_path = backend_report_path if os.path.exists(backend_report_path) else os.path.join(UPLOAD_DIR, f"{report_id}.json")
    
    if os.path.exists(report_path):
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading report: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail=f"Report not found for ID: {report_id}")

@app.get("/report/{report_id}")
async def redirect_to_report(report_id: str):
    """Redirect to the report page"""
    print(f"Redirecting to report for report_id: {report_id}")
    
    # Check if the report exists
    report_path = os.path.join(UPLOAD_DIR, f"{report_id}.json")
    if os.path.exists(report_path):
        return RedirectResponse(url=f"/api/report/{report_id}")
    else:
        raise HTTPException(status_code=404, detail=f"Report not found for ID: {report_id}")

@app.get("/api/languages")
async def get_supported_languages():
    """Return a list of supported languages for the application"""
    return {
        "languages": [{"name": lang, "code": code} for lang, code in SUPPORTED_LANGUAGES.items()]
    }


if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
