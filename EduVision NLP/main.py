import pandas as pd
import os
import sys
from datetime import datetime
import logging

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.gemini import GeminiReportGenerator
from prompts.report_prompt import build_classroom_prompt
from utils.formatter import ReportFormatter
from utils.csv_loader import CSVLoader

class EduVisionClassroomProcessor:
    """
    Main class to process CSV data from computer vision model and generate classroom reports.
    """
    
    def __init__(self):
        """Initialize the classroom report processor with all necessary components."""
        self.gemini_generator = GeminiReportGenerator()
        self.formatter = ReportFormatter()
        self.csv_loader = CSVLoader()
        self.logger = self._setup_logger()
        
        # Create output directories
        os.makedirs("reports", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def _setup_logger(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/eduvision.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def process_classroom(self, course_name: str, students_data: list) -> dict:
        """
        Process an entire classroom and generate a single report.
        
        Args:
            course_name (str): Name of the course/class
            students_data (list): List of student data dictionaries
            
        Returns:
            dict: Processing result with classroom report
        """
        try:
            self.logger.info(f"Processing classroom: {course_name} with {len(students_data)} students")
            
            # Prepare class info
            class_info = {
                'course_name': course_name,
                'session_time': students_data[0].get('session_time', 'Not specified'),
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
            # Build classroom prompt
            prompt = build_classroom_prompt(students_data, class_info)
            
            # Generate report with Gemini
            gemini_result = self.gemini_generator.generate_report(prompt)
            
            if not gemini_result['success']:
                return {
                    'success': False,
                    'course_name': course_name,
                    'error': gemini_result['error']
                }
            
            # Format the classroom report
            formatted_report = self.formatter.format_report(
                gemini_result['report'],
                f"Class: {course_name}",
                f"CLASSROOM_{course_name.replace(' ', '_')}"
            )
            
            return {
                'success': True,
                'course_name': course_name,
                'student_count': len(students_data),
                'students': [f"{s['name']} (ID-{s['student_id']})" for s in students_data],
                'formatted_report': formatted_report,
                'raw_report': gemini_result['report']
            }
            
        except Exception as e:
            self.logger.error(f"Error processing classroom {course_name}: {str(e)}")
            return {
                'success': False,
                'course_name': course_name,
                'error': str(e)
            }

    def process_csv_file(self, csv_file_path: str, save_reports: bool = True) -> dict:
        """Process CSV file by classroom instead of individual students."""
        try:
            # Load data using CSV loader
            df = self.csv_loader.load_csv(csv_file_path)
            
            # Get summary stats
            stats = self.csv_loader.get_summary_stats(df)
            self.logger.info(f"CSV Summary: {stats}")
            
            # Group by classroom
            classroom_batches = self.csv_loader.get_classroom_batches(df)
            
            results = {
                'total_classrooms': len(classroom_batches),
                'total_students': len(df),
                'csv_stats': stats,
                'successful_reports': 0,
                'failed_reports': 0,
                'errors': [],
                'classroom_reports': []
            }
            
            # Process each classroom
            for course_name, students_data in classroom_batches.items():
                self.logger.info(f"Processing {course_name} with {len(students_data)} students...")
                result = self.process_classroom(course_name, students_data)
                
                if result['success']:
                    results['successful_reports'] += 1
                    results['classroom_reports'].append(result)
                    
                    # Save classroom report
                    if save_reports:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"classroom_{course_name.replace(' ', '_')}_{timestamp}.txt"
                        
                        if self.formatter.save_formatted_report(result['formatted_report'], filename):
                            self.logger.info(f"✅ Saved report: {filename}")
                        else:
                            self.logger.warning(f"Failed to save report: {filename}")
                else:
                    results['failed_reports'] += 1
                    results['errors'].append({
                        'classroom': result['course_name'],
                        'error': result['error']
                    })
            
            # Generate summary report
            self._generate_summary_report(results, csv_file_path)
            
            self.logger.info(f"Processing complete: {results['successful_reports']}/{results['total_classrooms']} classrooms successful")
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing CSV file: {str(e)}")
            raise
    
    def _generate_summary_report(self, results: dict, csv_file_path: str):
        """Generate a summary report of the processing session."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary_filename = f"processing_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        summary_content = f"""
EDUVISION CLASSROOM PROCESSING SUMMARY
{'='*60}
Processing Date: {timestamp}
Source File: {csv_file_path}

CSV DATA OVERVIEW:
- Total Students: {results['csv_stats']['total_students']}
- Total Classrooms: {results['csv_stats']['unique_courses']}
- Average Attention Score: {results['csv_stats']['avg_attention_score']:.1f}%
- Students Needing Support: {results['csv_stats']['students_needing_support']}
- High Performers: {results['csv_stats']['high_performers']}

CLASSROOM BREAKDOWN:
"""
        
        for course, count in results['csv_stats']['course_breakdown'].items():
            summary_content += f"- {course}: {count} students\n"
        
        summary_content += f"""

PROCESSING STATISTICS:
- Total Classrooms Processed: {results['total_classrooms']}
- Successful Reports: {results['successful_reports']}
- Failed Reports: {results['failed_reports']}
- Success Rate: {(results['successful_reports']/results['total_classrooms']*100):.1f}%

"""
        
        if results['errors']:
            summary_content += "ERRORS:\n"
            for error in results['errors']:
                summary_content += f"- {error['classroom']}: {error['error']}\n"
        
        if results['successful_reports'] > 0:
            summary_content += "\nSUCCESSFUL CLASSROOM REPORTS:\n"
            for report in results['classroom_reports']:
                summary_content += f"- {report['course_name']}: {report['student_count']} students\n"
                summary_content += f"  Students: {', '.join(report['students'][:3])}{'...' if len(report['students']) > 3 else ''}\n"
        
        # Save summary
        try:
            with open(f"reports/{summary_filename}", 'w', encoding='utf-8') as f:
                f.write(summary_content)
            self.logger.info(f"📋 Summary report saved: {summary_filename}")
        except Exception as e:
            self.logger.error(f"Failed to save summary: {str(e)}")

def main():
    """Main function to run the EduVision classroom processor."""
    print("🚀 EduVision Classroom Report Processor")
    print("="*60)
    
    processor = EduVisionClassroomProcessor()
    
    # Get CSV file path
    csv_file_path = input("Enter path to CSV file (or press Enter for example): ").strip()
    
    if not csv_file_path:
        # Use the example CSV created by csv_loader
        csv_file_path = 'example_cv_data.csv'
        if not os.path.exists(csv_file_path):
            print("Creating example CSV file...")
            csv_file_path = processor.csv_loader.create_example_csv()
        print(f"Using example CSV: {csv_file_path}")
    
    try:
        # Test Gemini connection first
        print("\n🔍 Testing Gemini API connection...")
        if not processor.gemini_generator.test_connection():
            print("❌ Failed to connect to Gemini API. Check your API key in config.py")
            return
        
        print("✅ Gemini API connection successful!")
        
        # Validate CSV format first
        print(f"\n📊 Validating CSV format...")
        validation = processor.csv_loader.validate_csv_format(csv_file_path)
        
        if not validation['valid']:
            print(f"❌ CSV validation failed: {validation.get('error', 'Invalid format')}")
            return
        
        print(f"✅ CSV valid: {validation['total_rows']} rows, {len(validation['available_optional_columns'])} optional columns")
        
        # Process the CSV
        print(f"\n⚡ Processing classroom reports...")
        results = processor.process_csv_file(csv_file_path)
        
        # Display results
        print(f"\n📊 PROCESSING COMPLETE:")
        print(f"✅ Successful Classrooms: {results['successful_reports']}")
        print(f"❌ Failed Classrooms: {results['failed_reports']}")
        print(f"👥 Total Students: {results['total_students']}")
        print(f"📁 Reports saved in 'reports/' directory")
        
        # Show classroom details
        if results['classroom_reports']:
            print(f"\n📋 CLASSROOM REPORTS GENERATED:")
            for report in results['classroom_reports']:
                print(f"  🏫 {report['course_name']}: {report['student_count']} students")
                print(f"     Students: {', '.join(report['students'][:3])}{'...' if len(report['students']) > 3 else ''}")
        
        if results['errors']:
            print(f"\n❌ ERRORS:")
            for error in results['errors']:
                print(f"  - {error['classroom']}: {error['error']}")
        
    except FileNotFoundError:
        print(f"❌ CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        processor.logger.error(f"Main error: {str(e)}")

if __name__ == "__main__":
    main()