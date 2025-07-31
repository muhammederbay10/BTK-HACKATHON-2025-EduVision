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
                logging.FileHandler('logs/eduvision.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def process_classroom(self, course_name: str, students_data: list) -> dict:
        """
        Process a single classroom and generate detailed AI report.
        
        Args:
            course_name (str): Name of the course/classroom
            students_data (list): List of student data dictionaries
            
        Returns:
            dict: Processing results with detailed report
        """
        try:
            self.logger.info(f"Processing classroom: {course_name} with {len(students_data)} students")
            
            # Build comprehensive class info
            class_info = {
                'course_name': course_name,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'session_time': students_data[0].get('session_time', 'Unknown') if students_data else 'Unknown',
                'total_students': len(students_data)
            }
            
            # Generate the detailed prompt
            prompt = build_classroom_prompt(students_data, class_info)
            
            # Debug: Log prompt length and preview
            self.logger.info(f"Generated prompt length: {len(prompt)} characters")
            self.logger.info(f"Prompt preview: {prompt[:200]}...")
            
            # Generate AI report with detailed prompt
            ai_result = self.gemini_generator.generate_report(
                prompt=prompt,
                temperature=0.7
            )
            
            if not ai_result['success']:
                self.logger.error(f"AI report generation failed: {ai_result.get('error', 'Unknown error')}")
                return {
                    'success': False,
                    'error': f"AI generation failed: {ai_result.get('error', 'Unknown error')}",
                    'course_name': course_name,
                    'student_count': len(students_data)
                }
            
            # Get the raw AI report
            raw_ai_report = ai_result['report']
            self.logger.info(f"AI report generated successfully. Length: {len(raw_ai_report)} characters")
            self.logger.info(f"AI report preview: {raw_ai_report[:300]}...")
            
            # Format the report properly
            formatted_report = self.formatter.format_report(
                raw_report=raw_ai_report,
                class_name=course_name,
                class_id=course_name.replace(' ', '_')
            )
            
            # Create student summary for easy reference
            student_list = []
            student_names = []
            for student in students_data:
                student_id = student['student_id']
                student_name = student['name']
                student_list.append(f"{student_name} (ID-{student_id})")
                student_names.append(student_name)
            
            return {
                'success': True,
                'course_name': course_name,
                'student_count': len(students_data),
                'students': student_list,
                'student_names': student_names,
                'raw_ai_report': raw_ai_report,
                'formatted_report': formatted_report,
                'class_info': class_info,
                'processing_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error processing classroom {course_name}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'error': str(e),
                'course_name': course_name,
                'student_count': len(students_data) if students_data else 0
            }


    def process_csv_file(self, csv_file_path: str, save_reports: bool = True) -> dict:
        """
        Process CSV file and generate classroom reports.
        
        Args:
            csv_file_path (str): Path to the CSV file
            save_reports (bool): Whether to save reports to files
            
        Returns:
            dict: Processing results
        """
        try:
            # Load and validate CSV
            df = self.csv_loader.load_csv(csv_file_path)
            stats = self.csv_loader.get_summary_stats(df)
            
            self.logger.info(f"CSV Summary: {stats}")
            
            # Get classroom batches
            classroom_batches = self.csv_loader.get_classroom_batches(df)
            
            if not classroom_batches:
                return {
                    'success': False,
                    'error': 'No valid classroom data found',
                    'total_students': 0,
                    'successful_reports': 0,
                    'failed_reports': 0
                }
            
            # Process each classroom
            results = {
                'successful_reports': 0,
                'failed_reports': 0,
                'total_classrooms': len(classroom_batches),
                'total_students': len(df),  # Keep original student count
                'classroom_reports': [],
                'errors': []
            }
            
            for course_name, students_data in classroom_batches.items():
                self.logger.info(f"Processing {course_name} with {len(students_data)} students...")
                
                # Process this classroom
                classroom_result = self.process_classroom(course_name, students_data)
                
                if classroom_result['success']:
                    results['successful_reports'] += 1
                    results['classroom_reports'].append(classroom_result)
                    
                    # Save individual classroom report
                    if save_reports:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"classroom_{course_name.replace(' ', '_')}_{timestamp}.txt"
                        filepath = os.path.join('reports', filename)
                        
                        # Create comprehensive report content
                        report_content = f"""EDUVISION CLASSROOM ANALYSIS REPORT
    {'='*60}
    Course: {course_name}
    Date: {classroom_result['class_info']['date']}
    Session Time: {classroom_result['class_info']['session_time']}
    Students Analyzed: {classroom_result['student_count']}

    STUDENT LIST:
    {chr(10).join([f"- {student}" for student in classroom_result['students']])}

    {'='*60}
    AI-GENERATED CLASSROOM ANALYSIS:
    {'='*60}

    {classroom_result['raw_ai_report']}

    {'='*60}
    REPORT SECTIONS:
    {'='*60}

    CLASSROOM OVERVIEW:
    {classroom_result['formatted_report'].get('classroom_overview', 'Not available')}

    INDIVIDUAL STUDENT INSIGHTS:
    {classroom_result['formatted_report'].get('individual_analysis', 'Not available')}

    ENGAGEMENT PATTERNS:
    {classroom_result['formatted_report'].get('engagement_patterns', 'Not available')}

    RECOMMENDATIONS:
    {classroom_result['formatted_report'].get('recommendations', 'Not available')}

    INTERVENTION PRIORITIES:
    {classroom_result['formatted_report'].get('intervention_priorities', 'Not available')}

    {'='*60}
    Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    EduVision Classroom Analytics System
    """
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(report_content)
                        
                        self.logger.info(f"Saved report: {filename}")
                        
                else:
                    results['failed_reports'] += 1
                    results['errors'].append({
                        'classroom': course_name,
                        'error': classroom_result['error']
                    })
                    self.logger.error(f"Failed to process {course_name}: {classroom_result['error']}")
            
            # Generate summary report
            if save_reports:
                self._generate_summary_report(results, csv_file_path)
            
            self.logger.info(f"Processing complete: {results['successful_reports']}/{results['total_classrooms']} classrooms successful")
            
            return results
            
        except Exception as e:
            error_msg = f"Error processing CSV file: {str(e)}"
            self.logger.error(error_msg)
            raise

    def _generate_summary_report(self, results: dict, csv_file_path: str):
        """
        Generate a summary report of the processing session.
        
        Args:
            results (dict): Processing results
            csv_file_path (str): Path to the source CSV file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            summary_filename = f"processing_summary_{timestamp}.txt"
            summary_filepath = os.path.join('reports', summary_filename)
            
            # Calculate success rate
            total_classrooms = results['total_classrooms']
            success_rate = (results['successful_reports'] / total_classrooms * 100) if total_classrooms > 0 else 0
            
            summary_content = f"""EDUVISION CLASSROOM PROCESSING SUMMARY
    {'='*60}
    Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Source File: {csv_file_path}

    CSV DATA OVERVIEW:
    - Total Students: {results['total_students']}
    - Total Classrooms: {total_classrooms}
    - Success Rate: {success_rate:.1f}%

    PROCESSING STATISTICS:
    - Total Classrooms Processed: {total_classrooms}
    - Successful Reports: {results['successful_reports']}
    - Failed Reports: {results['failed_reports']}

    """

            # Add successful classroom details
            if results['classroom_reports']:
                summary_content += "SUCCESSFUL CLASSROOM REPORTS:\n"
                for report in results['classroom_reports']:
                    summary_content += f"- {report['course_name']}: {report['student_count']} students\n"
                    summary_content += f"  Students: {', '.join(report['students'][:3])}{'...' if len(report['students']) > 3 else ''}\n"
                    summary_content += f"  Report Length: {len(report['raw_ai_report'])} characters\n"
                    summary_content += f"  Processing Time: {report['processing_time']}\n\n"
            
            # Add error details if any
            if results['errors']:
                summary_content += "PROCESSING ERRORS:\n"
                for error in results['errors']:
                    summary_content += f"- {error['classroom']}: {error['error']}\n"
            
            summary_content += f"""
    {'='*60}
    Summary Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    EduVision Classroom Analytics System
    """
            
            # Save summary report
            with open(summary_filepath, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            self.logger.info(f"Summary report saved: {summary_filename}")
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")

def main():
    """Main function to run the EduVision classroom processor."""
    print("🚀 EduVision Classroom Report Processor")
    print("="*60)
    
    processor = EduVisionClassroomProcessor()
    
    # Get CSV file path
    csv_file_path = input("Enter path to CSV file (or press Enter for example): ").strip()
    
    if not csv_file_path:
        csv_file_path = 'EduVision NLP/data/student_attention_log.csv'
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