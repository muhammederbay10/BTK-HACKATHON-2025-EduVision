import os
import sys
import json
import datetime
import threading

# Import needed for type annotations
from typing import Dict, Any

# Define supported languages
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

# Add project root and module paths to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cv_module_path = os.path.join(project_root, "computer-vision_integration")
nlp_module_path = os.path.join(project_root, "EduVision_NLP")

# Make sure the paths exist in Python's search path
if cv_module_path not in sys.path:
    sys.path.insert(0, cv_module_path)
if nlp_module_path not in sys.path:
    sys.path.insert(0, nlp_module_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the required modules directly with their full file paths
import importlib.util
import importlib.machinery

# Load attention_tracker (now main.py)
attention_tracker_path = os.path.join(cv_module_path, "main.py")

# Construct the full path to the attention_tracker.py module
cv_module_path = os.path.join(os.path.dirname(__file__), "computer-vision_integration")
attention_tracker_path = os.path.join(cv_module_path, "attention_tracker.py")


loader = importlib.machinery.SourceFileLoader("attention_tracker", attention_tracker_path)
attention_tracker = loader.load_module()
attention_tracker_main = attention_tracker.main

# Load EduVisionClassroomProcessor 
nlp_module_path = os.path.join(os.path.dirname(__file__), "EduVision_NLP", "main.py")
loader = importlib.machinery.SourceFileLoader("nlp_main", nlp_module_path)
nlp_main = loader.load_module()
EduVisionClassroomProcessor = nlp_main.EduVisionClassroomProcessor

# Dictionary to store processing status
processing_status: Dict[str, str] = {}

def process_video_task(video_id: str, video_path: str, upload_dir: str, course_name: str = "test_lesson", language: str = "turkish") -> None:
    """Process video in a separate thread"""
    try:
        processing_status[video_id] = "processing"
        # Always use .csv extension
        csv_path = os.path.join(upload_dir, f"{video_id}.csv")
        report_path = os.path.join(upload_dir, f"{video_id}.json")
        
        print(f"🎬 Processing video {video_id}")
        print(f"📚 Course: '{course_name}'")
        print(f"🌍 Language: {language}")
        print(f"🧵 Background thread started")
        
        # Process video directly using attention_tracker module
        print(f"Running computer vision processing on {video_path}")
        print(f"Output CSV: {csv_path}")
        
        # Save original sys.argv and set new ones for attention_tracker.main()
        original_argv = sys.argv
        sys.argv = [
            'attention_tracker.py',
            '--video_path', video_path,
            '--output_csv', csv_path
        ]
        
        try:
            # Call the main function from the attention_tracker module
            attention_tracker_main()
            print("Computer vision processing finished.")
        finally:
            # Restore original sys.argv
            sys.argv = original_argv
        
        # Verify that CV script actually generated the CSV
        print("Running NLP processing...")
        
        try:
            # Verify CSV exists before processing
            if not os.path.exists(csv_path):
                print(f"Error: CSV file not found at {csv_path}")
                return
            
            # Use EduVisionClassroomProcessor directly
            processor = EduVisionClassroomProcessor()
            
            # Use absolute paths to avoid path resolution issues
            abs_csv_path = os.path.abspath(csv_path)
            abs_report_path = os.path.abspath(report_path)
            
            print(f"Processing CSV: {abs_csv_path}")
            print(f"Output JSON: {abs_report_path}")
            print(f"Course Name: {course_name}")
            print(f"Language: {language}")
            
            # Process the CSV directly using the processor with course name and language
            results = processor.process_csv_file(abs_csv_path, course_name=course_name, language=language.lower())         

            # If we have classroom reports, use the first one to generate our JSON output
            if results['successful_reports'] > 0 and results['classroom_reports']:
                report = results['classroom_reports'][0]
                # Parse the AI report into structured sections
                parsed_sections = processor._parse_ai_report_to_sections(report['raw_ai_report'])
                
                # Get attention over time analysis from the report
                students_data = processor._generate_attention_over_time_analysis(report['students_data']) if hasattr(report, 'students_data') else {}
                
                # Create structured JSON report with parsed sections and additional analysis
                json_report = {
                    "report_metadata": {
                        "report_type": "EduVision Classroom Analysis",
                        "course_name": report['course_name'],
                        "date": report['class_info']['date'],
                        "session_time": str(report['class_info']['session_time']),
                        "students_analyzed": report['student_count'],
                        "generated_at": datetime.datetime.now().isoformat(),
                        "processing_time": report['processing_time'],
                        "video_id": video_id,
                        "language": language
                    },
                    "student_summary": {
                        "total_students": report['student_count'],
                        "student_list": report.get('student_names', [])
                    },
                    "ai_analysis": {
                        "executive_summary": parsed_sections.get('executive_summary', 'Not available'),
                        "individual_student_analysis": parsed_sections.get('individual_analysis', 'Not available'),
                        "temporal_analysis": parsed_sections.get('temporal_analysis', 'Not available'),
                        "classroom_dynamics": parsed_sections.get('classroom_dynamics', 'Not available'),
                        "actionable_recommendations": parsed_sections.get('recommendations', 'Not available'),
                        "metrics_summary": parsed_sections.get('metrics_summary', 'Not available')
                    },
                    "attention_over_time": students_data,
                    "data_insights": {
                        "report_id": video_id
                    }
                }
                
                # Make sure there's a reports directory in the backend
                backend_reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
                os.makedirs(backend_reports_dir, exist_ok=True)
                
                # Save a copy of the report in the backend reports directory
                backend_report_path = os.path.join(backend_reports_dir, f"{video_id}.json")
                
                # Write the JSON report to both locations
                with open(abs_report_path, 'w', encoding='utf-8') as f:
                    json.dump(json_report, f, indent=2, ensure_ascii=False)
                
                with open(backend_report_path, 'w', encoding='utf-8') as f:
                    json.dump(json_report, f, indent=2, ensure_ascii=False)
                
                print(f"JSON report saved to: {abs_report_path}")
                print(f"JSON report also saved to backend reports: {backend_report_path}")
            else:
                # Handle case where no reports were generated
                error_data = {
                    "error": "Failed to generate classroom reports",
                    "status": "error",
                    "message": f"No classroom reports were generated from the CSV data",
                    "video_id": video_id
                }
                
                with open(abs_report_path, 'w') as f:
                    json.dump(error_data, f, indent=2)
                
                # Create backend reports directory and save error report there as well
                backend_reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
                os.makedirs(backend_reports_dir, exist_ok=True)
                backend_report_path = os.path.join(backend_reports_dir, f"{video_id}.json")
                
                with open(backend_report_path, 'w') as f:
                    json.dump(error_data, f, indent=2)
                
            print("NLP processing finished.")
            
        except Exception as e:
            print(f"Error running NLP script: {e}")
            # Create a minimal JSON report with error info
            with open(report_path, 'w') as f:
                json.dump({
                    "error": str(e),
                    "status": "failed",
                    "message": "Failed to process video",
                    "video_id": video_id
                }, f)
            
        # Update status after processing is done
        if os.path.exists(report_path):
            processing_status[video_id] = "completed"
            print(f"Processing completed for video_id: {video_id}, course: {course_name}, language: {language}")
        else:
            processing_status[video_id] = "error"
            print(f"Failed to generate report for video_id: {video_id}")
        
    except Exception as e:
        print(f"Error during processing video {video_id}: {e}")
        processing_status[video_id] = "error"
        # Try to create an error report
        try:
            error_data = {
                "error": str(e),
                "status": "error",
                "message": "Failed to process video",
                "video_id": video_id
            }
            
            # Save in upload directory
            with open(os.path.join(upload_dir, f"{video_id}.json"), 'w') as f:
                json.dump(error_data, f, indent=2)
                
            # Also save in backend reports directory
            backend_reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
            os.makedirs(backend_reports_dir, exist_ok=True)
            with open(os.path.join(backend_reports_dir, f"{video_id}.json"), 'w') as f:
                json.dump(error_data, f, indent=2)
                
        except Exception as save_error:
            print(f"Failed to save error report: {save_error}")

def get_status(report_id: str) -> str:
    """Get the processing status of a video"""
    return processing_status.get(report_id, "not found")