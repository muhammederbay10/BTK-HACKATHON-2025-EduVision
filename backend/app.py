import os
import uuid
import threading
import json
import psycopg2
from psycopg2 import sql
import hashlib
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Query, Cookie, Response, Depends # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import RedirectResponse # type: ignore
from typing import Optional

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

# Create logs and reports directories required by NLP script
project_root = os.path.dirname(BASE_DIR)
os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
os.makedirs(os.path.join(project_root, "reports"), exist_ok=True)
# Create reports directory in the backend folder too
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

# Database connection function
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="enes",
            password="postgres",
            port="5432"
        )
        connection.autocommit = True
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

# Password hashing function
def hash_password(password: str) -> str:
    # Create SHA-256 hash of the password
    return hashlib.sha256(password.encode()).hexdigest()

# Generate a random authentication token
def generate_auth_token() -> str:
    return str(uuid.uuid4())

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

@app.post("/api/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    response: Response = None
):
    """Register a new user"""
    print(f"[DEBUG] Signup attempt for email: {email}")
    # Hash the password
    hashed_password = hash_password(password)
    print(f"[DEBUG] Password hashed for user: {email}")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if user with this email already exists
        print(f"[DEBUG] Checking if email already exists: {email}")
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            print(f"[DEBUG] Email already exists: {email}")
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Generate auth token
        auth_token = generate_auth_token()
        print(f"[DEBUG] Auth token generated for: {email}")
        
        # Create new user with auth token
        print(f"[DEBUG] Inserting new user: {name}, {email}")
        cursor.execute(
            "INSERT INTO users (name, email, password, auth_token) VALUES (%s, %s, %s, %s) RETURNING id",
            (name, email, hashed_password, auth_token)
        )
        user_id = cursor.fetchone()[0]
        print(f"[DEBUG] User created with ID: {user_id}")
        
        # Generate and store auth token
        auth_token = generate_auth_token()
        print(f"[DEBUG] Updating auth token for user ID: {user_id}")
        cursor.execute(
            "UPDATE users SET auth_token = %s WHERE id = %s",
            (auth_token, user_id)
        )
        
        cursor.close()
        conn.close()
        
        # Set auth cookie
        print(f"[DEBUG] Setting auth cookie for user ID: {user_id}")
        response.set_cookie(
            key="auth_token", 
            value=auth_token, 
            httponly=True, 
            secure=False,  # Set to True in production with HTTPS
            max_age=604800  # 7 days
        )
        
        print(f"[DEBUG] User registration successful: {user_id}")
        return {"message": "User registered successfully", "userId": user_id}
        
    except Exception as e:
        print(f"[ERROR] Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    response: Response = None
):
    """Log in a user"""
    print(f"[DEBUG] Login attempt for email: {email}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the provided password
        hashed_password = hash_password(password)
        print(f"[DEBUG] Password hashed for login attempt: {email}")
        
        # Find user
        print(f"[DEBUG] Looking up user with email: {email}")
        cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"[DEBUG] User not found: {email}")
            cursor.close()
            conn.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if user[1] != hashed_password:
            print(f"[DEBUG] Invalid password for user: {email}")
            cursor.close()
            conn.close()
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user_id = user[0]
        print(f"[DEBUG] Valid credentials for user ID: {user_id}")
        
        # Generate and store new auth token
        auth_token = generate_auth_token()
        print(f"[DEBUG] Generated auth token for user ID: {user_id}")
        cursor.execute(
            "UPDATE users SET auth_token = %s WHERE id = %s",
            (auth_token, user_id)
        )
        print(f"[DEBUG] Updated auth token in database for user ID: {user_id}")
        
        cursor.close()
        conn.close()
        
        # Set auth cookie
        print(f"[DEBUG] Setting auth cookie for user ID: {user_id}")
        response.set_cookie(
            key="auth_token", 
            value=auth_token, 
            httponly=True, 
            secure=False,  # Set to True in production with HTTPS
            max_age=604800  # 7 days
        )
        
        print(f"[DEBUG] Login successful for user ID: {user_id}")
        return {"message": "Login successful", "userId": user_id}
        
    except Exception as e:
        print(f"[ERROR] Error during login: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/api/logout")
async def logout(response: Response):
    """Log out the current user"""
    response.delete_cookie(key="auth_token")
    return {"message": "Logged out successfully"}

@app.get("/api/me")
async def get_current_user(auth_token: str = Cookie(None)):
    """Get current user information"""
    if not auth_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email FROM users WHERE auth_token = %s", (auth_token,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication")
            
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
        
    except Exception as e:
        print(f"Error getting current user: {e}")
        raise HTTPException(status_code=500, detail="Authentication error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port)
