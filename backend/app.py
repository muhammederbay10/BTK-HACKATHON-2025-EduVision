import os
import uuid
import threading
import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import RedirectResponse # type: ignore

# Import video processor module
from video_processor import process_video_task, get_status, SUPPORTED_LANGUAGES

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

# Create logs directory required by NLP script
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Dictionary to store processing status
processing_status = {}

# Supported languages
SUPPORTED_LANGUAGES = {
    "english": "en",
    "turkish": "tr", 
    "arabic": "ar",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "portuguese": "pt",
    "chinese": "zh",
    "japanese": "ja",
    "russian": "ru"
}

def process_video_task(video_id, video_path, course_name="API_Upload", language="english"):
    """Process video in a separate thread"""
    try:
        processing_status[video_id] = "processing"
        transcript_path = os.path.join(UPLOAD_DIR, f"{video_id}.txt")
        report_path = os.path.join(UPLOAD_DIR, f"{video_id}.json")
        
        print(f"🎬 Processing video {video_id}")
        print(f"📚 Course: '{course_name}'")
        print(f"🌍 Language: {language}")
        print(f"🧵 Background thread started")

        # Use correct paths to scripts based on project structure
        project_root = os.path.dirname(os.path.dirname(__file__))
        cv_script = os.path.join(project_root, "computer-vision_integration", "attention_tracker.py")
        
        # Make sure the paths exist
        if not os.path.exists(cv_script):
            print(f"Warning: CV script not found at {cv_script}")
            # Attempt to search for the script
            for root, dirs, files in os.walk(project_root):
                if "attention_tracker.py" in files:
                    cv_script = os.path.join(root, "attention_tracker.py")
                    print(f"Found CV script at: {cv_script}")
                    break
        
        # Use the same approach as in test_integration.py
        print(f"Running CV script: {cv_script}")
        print(f"With args: --video_path {video_path} --output_csv {transcript_path}")
        subprocess.run([
            sys.executable, str(cv_script),
            "--video_path", video_path,
            "--output_csv", transcript_path
        ], check=True)
        print("Computer vision script finished.")
        
        print("Running NLP script...")
        nlp_script = os.path.join(project_root, "EduVision NLP", "main.py")
        
        # Make sure the paths exist
        if not os.path.exists(nlp_script):
            print(f"Warning: NLP script not found at {nlp_script}")
            # Attempt to search for the script
            for root, dirs, files in os.walk(project_root):
                if "main.py" in files and "NLP" in root:
                    nlp_script = os.path.join(root, "main.py")
                    print(f"Found NLP script at: {nlp_script}")
                    break
        
        # Run NLP script with course name
        print(f"Running NLP script: {nlp_script}")
        print(f"With args: --csv_path {transcript_path} --course_name {course_name} --language {language}")
        
        # Set environment variable for logs directory to ensure NLP script uses correct logs path
        # Create logs directories in all potential locations the NLP script might be looking for
        nlp_logs_dir = os.path.join(project_root, "logs")
        os.makedirs(nlp_logs_dir, exist_ok=True)
        
        # Also create logs dir in backend folder, which seems to be where the script is looking
        backend_logs_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(backend_logs_dir, exist_ok=True)
        
        # Create logs inside NLP directory as well
        nlp_dir = os.path.dirname(nlp_script)
        nlp_internal_logs_dir = os.path.join(nlp_dir, "logs")
        os.makedirs(nlp_internal_logs_dir, exist_ok=True)
        
        # Create environment with custom LOGS_DIR
        env = os.environ.copy()
        env["LOGS_DIR"] = backend_logs_dir
        
        subprocess.run([
            sys.executable, str(nlp_script),
            "--csv_path", transcript_path,
            "--course_name", course_name,
            "--language", language
        ], check=True, env=env)
        print("NLP script finished.")
        
        # Update status after processing is done
        processing_status[video_id] = "completed"
        print(f"Processing completed for video_id: {video_id}, course: {course_name}, language: {language}")
        
    except Exception as e:
        print(f"Error during processing video {video_id}: {e}")
        processing_status[video_id] = "error"

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...), course_name: str = Query("API_Upload"), language: str = Query("english")):
    video_id = str(uuid.uuid4())
    print(f"Generated video_id: {video_id} for course '{course_name}'")
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
    
    # Initialize processing status
    processing_status[video_id] = "pending"

    # Validate language input
    if language.lower() not in SUPPORTED_LANGUAGES:
        print(f"⚠️ Unsupported language '{language}', defaulting to English.")
        language = "english"
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_video_task, 
        args=(video_id, video_path, course_name, language)
    )
    thread.daemon = True
    thread.start()
    
    # Return immediately with the video ID
    return {"reportId": video_id, "courseName": course_name, "language": language}

@app.post("/api/status/{report_id}")
async def force_processing_status(report_id: str, force: str = Query(None)):
    """Force update the processing status for a report"""
    print(f"Forcing status for report_id: {report_id} to {force}")
    
    if force == "completed":
        processing_status[report_id] = "completed"
        return {"status": "completed", "forced": True}
    else:
        raise HTTPException(status_code=400, detail="Invalid force value")

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
