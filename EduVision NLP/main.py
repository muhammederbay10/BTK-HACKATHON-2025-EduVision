import os
import sys
from datetime import datetime
import logging
import json

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
        # Create output directories
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs(os.path.join(project_root, "reports"), exist_ok=True)
        os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
        
        self.gemini_generator = GeminiReportGenerator()
        self.formatter = ReportFormatter()
        self.csv_loader = CSVLoader()
        self.logger = self._setup_logger()
    
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
        Process CSV file and generate classroom reports in JSON format.
        
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
                'total_students': len(df),
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
                    
                    # Save individual classroom report as JSON
                    if save_reports:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"classroom_{course_name.replace(' ', '_')}_{timestamp}.json"
                        filepath = os.path.join('reports', filename)
                        
                        # Parse the AI report into structured sections
                        parsed_sections = self._parse_ai_report_to_sections(classroom_result['raw_ai_report'])
                        
                        # Create structured JSON report with parsed sections
                        json_report = {
                            "report_metadata": {
                                "report_type": "EduVision Classroom Analysis",
                                "course_name": course_name,
                                "date": classroom_result['class_info']['date'],
                                "session_time": str(classroom_result['class_info']['session_time']),
                                "students_analyzed": classroom_result['student_count'],
                                "generated_at": datetime.now().isoformat(),
                                "processing_time": classroom_result['processing_time']
                            },
                            "student_summary": {
                                "total_students": classroom_result['student_count'],
                                "student_list": []
                            },
                            "ai_analysis": {
                                "executive_summary": parsed_sections.get('executive_summary', 'Not available'),
                                "individual_student_analysis": parsed_sections.get('individual_analysis', 'Not available'),
                                "temporal_analysis": parsed_sections.get('temporal_analysis', 'Not available'),
                                "classroom_dynamics": parsed_sections.get('classroom_dynamics', 'Not available'),
                                "actionable_recommendations": parsed_sections.get('recommendations', 'Not available'),
                                "metrics_summary": parsed_sections.get('metrics_summary', 'Not available')
                            },
                            "data_insights": {
                                "average_attention_score": round(sum(s['overall_attention_score'] for s in students_data) / len(students_data), 2),
                                "total_distractions": sum(s['total_distractions'] for s in students_data),
                                "high_performers": [s['name'] for s in students_data if s['overall_attention_score'] >= 80],
                                "needs_support": [s['name'] for s in students_data if s['overall_attention_score'] < 60],
                                "session_statistics": {
                                    "min_attention": min(s['overall_attention_score'] for s in students_data),
                                    "max_attention": max(s['overall_attention_score'] for s in students_data),
                                    "attention_range": max(s['overall_attention_score'] for s in students_data) - min(s['overall_attention_score'] for s in students_data)
                                }
                            }
                        }
                        
                        # Convert student data properly - handle timestamps
                        for student in students_data:
                            student_entry = {
                                "student_id": student['student_id'],
                                "name": student['name'],
                                "overall_attention_score": student['overall_attention_score'],
                                "total_distractions": student['total_distractions'],
                                "session_duration_minutes": student['total_session_minutes'],
                                "session_time": str(student.get('session_time', 'Unknown'))
                            }
                            json_report["student_summary"]["student_list"].append(student_entry)
                        
                        # Save as JSON with proper formatting
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(json_report, f, indent=2, ensure_ascii=False)
                        
                        self.logger.info(f"📄 Saved JSON report: {filename}")
                        
                else:
                    results['failed_reports'] += 1
                    results['errors'].append({
                        'classroom': course_name,
                        'error': classroom_result['error']
                    })
                    self.logger.error(f"Failed to process {course_name}: {classroom_result['error']}")
            
            # Generate summary report as JSON
            if save_reports:
                self._generate_summary_report_json(results, csv_file_path)
            
            self.logger.info(f"Processing complete: {results['successful_reports']}/{results['total_classrooms']} classrooms successful")
            
            return results
            
        except Exception as e:
            error_msg = f"Error processing CSV file: {str(e)}"
            self.logger.error(error_msg)
            raise

    def _parse_ai_report_to_sections(self, raw_report: str) -> dict:
        """
        Parse the raw AI report into structured sections.
        
        Args:
            raw_report (str): The raw AI-generated report
            
        Returns:
            dict: Parsed sections
        """
        try:
            sections = {}
            lines = raw_report.split('\n')
            current_section = None
            current_content = []
            
            # Define section mappings
            section_headers = {
                'executive_summary': ['1. EXECUTIVE SUMMARY', 'EXECUTIVE SUMMARY'],
                'individual_analysis': ['2. INDIVIDUAL STUDENT ANALYSIS', 'INDIVIDUAL STUDENT ANALYSIS'],
                'temporal_analysis': ['3. TEMPORAL ANALYSIS', 'TEMPORAL ANALYSIS'],
                'classroom_dynamics': ['4. CLASSROOM DYNAMICS', 'CLASSROOM DYNAMICS'],
                'recommendations': ['5. ACTIONABLE RECOMMENDATIONS', 'ACTIONABLE RECOMMENDATIONS'],
                'metrics_summary': ['6. METRICS SUMMARY', 'METRICS SUMMARY']
            }
            
            for line in lines:
                line_clean = line.strip()
                
                # Check if this line is a section header
                found_section = None
                for section_key, headers in section_headers.items():
                    for header in headers:
                        if header in line_clean and line_clean.startswith('**'):
                            found_section = section_key
                            break
                    if found_section:
                        break
                
                if found_section:
                    # Save previous section if exists
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = found_section
                    current_content = []
                else:
                    # Add content to current section (skip header lines)
                    if current_section and line_clean and not line_clean.startswith('**'):
                        current_content.append(line)
            
            # Save the last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            return sections
            
        except Exception as e:
            self.logger.error(f"Error parsing AI report: {str(e)}")
            return {
                'executive_summary': raw_report,
                'individual_analysis': 'Parsing failed - see executive summary',
                'temporal_analysis': 'Parsing failed - see executive summary',
                'classroom_dynamics': 'Parsing failed - see executive summary',
                'recommendations': 'Parsing failed - see executive summary',
                'metrics_summary': 'Parsing failed - see executive summary'
            }
        
    def _generate_summary_report_json(self, results: dict, csv_file_path: str):
        """
        Generate a summary report in JSON format.
        
        Args:
            results (dict): Processing results
            csv_file_path (str): Path to the source CSV file
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            summary_filename = f"processing_summary_{timestamp}.json"
            summary_filepath = os.path.join('reports', summary_filename)
            
            # Calculate success rate
            total_classrooms = results['total_classrooms']
            success_rate = (results['successful_reports'] / total_classrooms * 100) if total_classrooms > 0 else 0
            
            # Create structured summary
            summary_json = {
                "processing_summary": {
                    "metadata": {
                        "processing_date": datetime.now().isoformat(),
                        "source_file": csv_file_path,
                        "eduvision_version": "1.0",
                        "report_type": "Processing Summary"
                    },
                    "statistics": {
                        "total_students": results['total_students'],
                        "total_classrooms": total_classrooms,
                        "success_rate_percentage": round(success_rate, 1),
                        "successful_reports": results['successful_reports'],
                        "failed_reports": results['failed_reports']
                    },
                    "successful_classrooms": [
                        {
                            "course_name": report['course_name'],
                            "student_count": report['student_count'],
                            "students": report['students'],
                            "report_length_chars": len(report['raw_ai_report']),
                            "processing_time": report['processing_time']
                        }
                        for report in results['classroom_reports']
                    ],
                    "errors": results['errors'] if results['errors'] else [],
                    "processing_notes": {
                        "total_processing_time": f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        "system": "EduVision Classroom Analytics"
                    }
                }
            }
            
            # Save summary as JSON
            with open(summary_filepath, 'w', encoding='utf-8') as f:
                json.dump(summary_json, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📋 Summary JSON report saved: {summary_filename}")
        
        except Exception as e:
            self.logger.error(f"Error generating JSON summary report: {str(e)}")

def main():
    """Main function to run the EduVision classroom processor."""
    print("🚀 EduVision Classroom Report Processor")
    print("="*60)
    
    processor = EduVisionClassroomProcessor()
    
    # Get CSV file path
    csv_file_path = input("Enter path to CSV file (or press Enter for example): ").strip()
    
    if not csv_file_path:
        csv_file_path = 'EduVision NLP/data/student_attention_log2.csv'
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