#!/usr/bin/env python3
"""
Test script to verify the integration between computer vision and NLP components.
This script demonstrates the complete pipeline: video -> CSV -> report
"""

import sys
import os
import subprocess
from pathlib import Path
import time

def test_pipeline_integration():
    """Test the complete video processing pipeline"""
    print("🧪 Testing EduVision Pipeline Integration")
    print("="*60)
    
    # Paths
    project_root = Path(__file__).parent
    cv_script = project_root / "computer-vision_integration" / "attention_tracker.py"
    nlp_script = project_root / "EduVision NLP" / "main.py"
    test_video = str(project_root / "vedio.mp4")
    
    if not test_video or not os.path.exists(test_video):
        print(f"❌ Video file not found at: {test_video}")
        return
    
    # Step 1: Run computer vision analysis
    print(f"\n🎯 Step 1: Running computer vision analysis...")
    csv_output = project_root / f"test_attention_log_{int(time.time())}.csv"
    
    try:
        cv_result = subprocess.run([
            sys.executable, str(cv_script),
            "--video_path", test_video,
            "--output_csv", str(csv_output)
        ], capture_output=True, text=True, timeout=300)
        
        if cv_result.returncode != 0:
            print(f"❌ Computer vision failed: {cv_result.stderr}")
            return
        
        print(f"✅ Computer vision completed. CSV saved to: {csv_output}")
        
    except subprocess.TimeoutExpired:
        print("❌ Computer vision processing timed out")
        return
    except Exception as e:
        print(f"❌ Error running computer vision: {e}")
        return
    
    # Step 2: Run NLP analysis
    print(f"\n🧠 Step 2: Running NLP analysis...")
    
    try:
        nlp_result = subprocess.run([
            sys.executable, str(nlp_script),
            "--csv_path", str(csv_output),
            "--course_name", "Test_Course"
        ], capture_output=True, text=True, timeout=300)
        
        if nlp_result.returncode != 0:
            print(f"❌ NLP processing failed: {nlp_result.stderr}")
            return
        
        print(f"✅ NLP analysis completed")
        
        # Find the generated report
        reports_dir = project_root / "reports"
        report_files = list(reports_dir.glob("classroom_Test_Course_*.txt"))
        
        if report_files:
            latest_report = max(report_files, key=os.path.getctime)
            print(f"📄 Report generated: {latest_report}")
            
            # Display report content
            print(f"\n📋 GENERATED REPORT CONTENT:")
            print("="*60)
            with open(latest_report, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
            print("="*60)
        else:
            print("❌ No report file found")
            
    except subprocess.TimeoutExpired:
        print("❌ NLP processing timed out")
        return
    except Exception as e:
        print(f"❌ Error running NLP: {e}")
        return
    
    print(f"\n🎉 Pipeline integration test completed successfully!")

if __name__ == "__main__":
    test_pipeline_integration()