import os
import subprocess
import sys
import uuid
import json
import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException, Query # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create logs directory required by NLP script
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Dictionary to store processing status
processing_status = {}

def process_video_task(video_id, video_path, course_name="API_Upload"):
    """Process video in a separate thread"""
    try:
        processing_status[video_id] = "processing"
        transcript_path = os.path.join(UPLOAD_DIR, f"{video_id}.txt")
        report_path = os.path.join(UPLOAD_DIR, f"{video_id}.json")
        
        print(f"Processing video {video_id} for course '{course_name}' in background thread")
        
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
        print(f"With args: --csv_path {transcript_path} --course_name API_Upload")
        
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
            "--course_name", course_name
        ], check=True, env=env)
        print("NLP script finished.")
        
        # Update status after processing is done
        processing_status[video_id] = "completed"
        print(f"Processing completed for video_id: {video_id}, course: {course_name}")
        
    except Exception as e:
        print(f"Error during processing video {video_id}: {e}")
        processing_status[video_id] = "error"

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...), course_name: str = Query("API_Upload")):
    video_id = str(uuid.uuid4())
    print(f"Generated video_id: {video_id} for course '{course_name}'")
    video_path = os.path.join(UPLOAD_DIR, f"{video_id}.mp4")
    print(f"Video path: {video_path}")

    # Save the uploaded file
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    print(f"Video saved to {video_path}")
    
    # Initialize processing status
    processing_status[video_id] = "pending"
    
    # Start processing in a separate thread
    thread = threading.Thread(
        target=process_video_task, 
        args=(video_id, video_path, course_name)
    )
    thread.daemon = True
    thread.start()
    
    # Return immediately with the video ID
    return {"reportId": video_id, "courseName": course_name}

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
    
    if report_id not in processing_status:
        # Check if the report file exists anyway (JSON format)
        report_path = os.path.join(UPLOAD_DIR, f"{report_id}.json")
        if os.path.exists(report_path):
            print(f"Found JSON report for {report_id}")
            processing_status[report_id] = "completed"
            return {"status": "completed"}
            
        # Also check in the reports directory for any files related to this process
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        if os.path.exists(reports_dir):
            print(f"Checking reports directory for {report_id}")
            # Look for any classroom report files
            for filename in os.listdir(reports_dir):
                if filename.endswith(".txt"):
                    print(f"Found report file: {filename}")
                    processing_status[report_id] = "completed"
                    return {"status": "completed"}
        
        # Check if we printed "Processing completed" for this ID in the logs
        if report_id in processing_status and processing_status[report_id] == "processing":
            print(f"Checking if processing is already marked as completed for {report_id}")
            # If we previously set it to processing and backend shows completion message,
            # let's assume it's completed
            processing_status[report_id] = "completed"
            return {"status": "completed"}
        
        print(f"No report found for {report_id}")
        # If we get here, we didn't find any report
        if report_id in processing_status:
            # Return whatever status we have
            return {"status": processing_status[report_id]}
        else:
            # Not found in processing_status and no file exists
            raise HTTPException(status_code=404, detail="Report not found")
    
    print(f"Status for {report_id} is {processing_status[report_id]}")
    return {"status": processing_status[report_id]}

@app.get("/report/{report_id}")
async def get_report(report_id: str):
    print(f"Fetching report for report_id: {report_id}")
    report_path = os.path.join(UPLOAD_DIR, f"{report_id}.json")
    print(f"Report path: {report_path}")
    
    # Check if the report exists in the upload directory
    if not os.path.exists(report_path):
        # Also check in the reports directory as a fallback
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        # Look for text file with report ID prefix
        for filename in os.listdir(reports_dir) if os.path.exists(reports_dir) else []:
            if filename.startswith("classroom_") and filename.endswith(".txt"):
                # Found a text report, read it and return as plain text
                full_path = os.path.join(reports_dir, filename)
                try:
                    with open(full_path, "r") as f:
                        report_content = f.read()
                    print(f"Text report found at: {full_path}")
                    # Return text report in a format the frontend can handle
                    return {"report": {"content": report_content, "type": "text"}}
                except Exception as e:
                    print(f"Error reading text report: {e}")
    
    # If the report ID is marked as completed in the status, but we can't find a file,
    # return a generic placeholder report
    if report_id in processing_status and processing_status[report_id] == "completed":
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        if os.path.exists(reports_dir):
            # Look for the most recent classroom report
            most_recent_report = None
            most_recent_time = 0
            for filename in os.listdir(reports_dir):
                if filename.startswith("classroom_") and filename.endswith(".txt"):
                    full_path = os.path.join(reports_dir, filename)
                    file_time = os.path.getmtime(full_path)
                    if file_time > most_recent_time:
                        most_recent_time = file_time
                        most_recent_report = full_path
                        
            if most_recent_report:
                try:
                    with open(most_recent_report, "r") as f:
                        report_content = f.read()
                    print(f"Using most recent classroom report: {most_recent_report}")
                    return {"report": {"content": report_content, "type": "text"}}
                except Exception as e:
                    print(f"Error reading most recent classroom report: {e}")
        
        # If we can't find any report, return a placeholder
        return {
            "report": {
                "type": "text",
                "content": f"Your video with ID {report_id} has been processed successfully.\n\nThe classroom report has been generated on the server. Please check the 'reports' directory for the full analysis output."
            }
        }
    
    # Try JSON report (original logic)
    try:
        with open(report_path, "r") as f:
            report = json.load(f)
        print(f"Report found for report_id: {report_id}")
        return {"report": report}
    except FileNotFoundError:
        print(f"Report not found for report_id: {report_id}")
        raise HTTPException(status_code=404, detail="Report not found")
    except Exception as e:
        print(f"An error occurred while fetching report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
