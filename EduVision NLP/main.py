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

    def process_classroom(self, course_name: str, students_data: list, language: str = "en") -> dict:
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
            prompt = build_classroom_prompt(students_data, class_info, language=language)
            
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
                'processing_time': datetime.now().isoformat(),
                'language': language
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

    def process_csv_file(self, csv_file_path: str, save_reports: bool = True, language: str = "en", course_name: str = None) -> dict:
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
            self.logger.info(f"Report Language: {language.title()}")
            
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
                'errors': [],
                'language': language,
                'course_name': course_name
            }
            
            for batch_name, students_data in classroom_batches.items():
                # user-provide course name or fallback to batch name
                actual_course_name = course_name if course_name else batch_name

                self.logger.info(f"Processing {course_name} with {len(students_data)} students...")
                
                # Process this classroom
                classroom_result = self.process_classroom(actual_course_name, students_data, language= language)
                
                if classroom_result['success']:
                    results['successful_reports'] += 1
                    results['classroom_reports'].append(classroom_result)
                    
                    # Save individual classroom report as JSON
                    if save_reports:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"classroom_{course_name.replace(' ', '')}{language}_{timestamp}.json"
                        filepath = os.path.join('reports', filename)
                        
                        # Parse the AI report into structured sections
                        parsed_sections = self._parse_ai_report_to_sections(classroom_result['raw_ai_report'])

                        # Generate attention over time analysis
                        attention_analysis = self._generate_attention_over_time_analysis(students_data)
                        
                        # Create structured JSON report with parsed sections
                        json_report = {
                            "report_metadata": {
                                "report_type": "EduVision Classroom Analysis",
                                "course_name": actual_course_name,
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
                            "attention_over_time": attention_analysis,
                            "data_insights": {
                                "average_attention_score": round(sum(s['overall_attention_score'] for s in students_data) / len(students_data), 2),
                                "total_distractions": int(sum(s['total_distractions'] for s in students_data)),
                                "high_performers": [str(s['name']) for s in students_data if s['overall_attention_score'] >= 80],
                                "needs_support": [str(s['name']) for s in students_data if s['overall_attention_score'] < 60],
                                "session_statistics": {
                                    "min_attention": float(min(s['overall_attention_score'] for s in students_data)),
                                    "max_attention": float(max(s['overall_attention_score'] for s in students_data)),
                                    "attention_range": float(max(s['overall_attention_score'] for s in students_data) - min(s['overall_attention_score'] for s in students_data))
                                }
                            }
                        }
                        
                        # Convert student data properly - handle timestamps
                        for student in students_data:
                            student_entry = {
                                "student_id": str(student['student_id']),
                                "name": str(student['name']),
                                "overall_attention_score": float(student['overall_attention_score']),
                                "total_distractions": int(student['total_distractions']),
                                "session_duration_minutes": float(student['total_session_minutes']),
                                "session_time": str(student.get('session_time', 'Unknown'))
                            }
                            json_report["student_summary"]["student_list"].append(student_entry)
                        
                        # Save as JSON with proper formatting
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(json_report, f, indent=2, ensure_ascii=False)
                        
                        self.logger.info(f"📄 Saved {language.title()} JSON report: {filename}")
                        
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
    
    def _generate_attention_over_time_analysis(self, students_data: list) -> dict:
        """
        Generate attention over time analysis for individual students and class ranking.
        
        Args:
            students_data (list): List of student data with time intervals
            
        Returns:
            dict: Attention over time analysis
        """
        try:
            # Individual student attention progression
            individual_progression = {}
            
            # Class-wide attention data for ranking
            class_attention_timeline = []
            
            for student in students_data:
                student_id = student['student_id']
                student_name = student['name']
                
                # Extract time intervals for this student
                time_intervals = student.get('time_intervals', [])
                
                progression = {
                    "student_info": {
                        "student_id": student_id,
                        "name": student_name,
                        "overall_score": student['overall_attention_score']
                    },
                    "time_progression": [],
                    "attention_trends": {},
                    "performance_metrics": {}
                }
                
                # Process each time interval
                interval_scores = []
                for i, interval in enumerate(time_intervals):
                    interval_data = {
                        "interval_number": int(i + 1),
                        "start_time": str(interval.get('interval_start', 'Unknown')),
                        "duration_minutes": float(interval.get('interval_duration_minutes', 3)),
                        "attention_rate": round(float(interval.get('attention_rate', 0)), 1),
                        "attention_status": str(interval.get('interval_status', 'Unknown')),
                        "distractions": int(interval.get('total_distractions', 0)),
                        "frames_analyzed": int(interval.get('frames_analyzed', 0))
                    }
                    
                    progression["time_progression"].append(interval_data)
                    interval_scores.append(float(interval.get('attention_rate', 0)))

                    # Add to class timeline for ranking
                    class_attention_timeline.append({
                        "student_id": student_id,
                        "student_name": student_name,
                        "interval": int(i + 1),
                        "time": str(interval.get('interval_start', 'Unknown')),
                        "attention_rate": float(interval.get('attention_rate', 0)),
                        "status": str(interval.get('interval_status', 'Unknown'))
                    })
                
                # Calculate attention trends
                if len(interval_scores) > 1:
                    # Trend analysis
                    start_score = interval_scores[0]
                    end_score = interval_scores[-1]
                    trend_change = end_score - start_score
                    
                    # Determine trend direction
                    if trend_change > 5:
                        trend = "Improving"
                    elif trend_change < -5:
                        trend = "Declining"
                    else:
                        trend = "Stable"
                    
                    progression["attention_trends"] = {
                        "overall_trend": trend,
                        "trend_change_percentage": round(trend_change, 1),
                        "highest_attention_interval": interval_scores.index(max(interval_scores)) + 1,
                        "lowest_attention_interval": interval_scores.index(min(interval_scores)) + 1,
                        "attention_variance": round(max(interval_scores) - min(interval_scores), 1)
                    }
                else:    
                    # Default values for single or no intervals
                    progression["attention_trends"] = {
                        "overall_trend": "Insufficient data",
                        "trend_change_percentage": 0.0,
                        "highest_attention_interval": 1 if interval_scores else 0,
                        "lowest_attention_interval": 1 if interval_scores else 0,
                        "attention_variance": 0.0
                    }
                # Performance metrics
                progression["performance_metrics"] = {
                    "average_attention": round(sum(interval_scores) / len(interval_scores), 1) if interval_scores else 0,
                    "peak_attention": max(interval_scores) if interval_scores else 0,
                    "lowest_attention": min(interval_scores) if interval_scores else 0,
                    "consistency_score": self._calculate_consistency_score(interval_scores),
                    "total_intervals": len(time_intervals)
                }
                
                individual_progression[student_id] = progression
            
            # Generate class-wide rankings
            class_rankings = self._generate_class_rankings(students_data, class_attention_timeline)
            
            return {
                "individual_student_progression": individual_progression,
                "class_rankings": class_rankings,
                "session_overview": {
                    "total_intervals_analyzed": len(class_attention_timeline),
                    "class_average_attention": round(sum([item['attention_rate'] for item in class_attention_timeline]) / len(class_attention_timeline), 1) if class_attention_timeline else 0,
                    "analysis_generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating attention over time analysis: {str(e)}")
            return {
                "error": f"Failed to generate attention over time analysis: {str(e)}",
                "individual_student_progression": {},
                "class_rankings": {},
                "session_overview": {
                    "total_intervals_analyzed": 0,
                    "class_average_attention": 0.0,
                    "analysis_generated_at": datetime.now().isoformat()
                }
            }

    def _calculate_consistency_score(self, scores: list) -> float:
        """
        Calculate consistency score based on variance in attention scores.
        Lower variance = higher consistency.
        
        Args:
            scores (list): List of attention scores
            
        Returns:
            float: Consistency score (0-100, higher is more consistent)
        """
        if not scores or len(scores) < 2:
            return 0.0
        
        # Calculate variance
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        
        # Convert variance to consistency score (inverse relationship)
        # Max expected variance is around 100 (0% to 100% attention range)
        consistency = max(0, 100 - (variance / 100) * 100)
        return round(consistency, 1)

    def _generate_class_rankings(self, students_data: list, class_timeline: list) -> dict:
        """
        Generate class-wide rankings and comparisons.
        
        Args:
            students_data (list): List of student data
            class_timeline (list): Timeline of all student attention data
            
        Returns:
            dict: Class rankings and analysis
        """
        try:
            # Overall performance ranking
            student_rankings = []
            for student in students_data:
                student_rankings.append({
                    "rank": 0,  # Will be assigned after sorting
                    "student_id": student['student_id'],
                    "student_name": student['name'],
                    "overall_attention_score": student['overall_attention_score'],
                    "total_distractions": student['total_distractions'],
                    "session_duration": student['total_session_minutes']
                })
            
            # Sort by attention score (descending)
            student_rankings.sort(key=lambda x: x['overall_attention_score'], reverse=True)
            
            # Assign ranks
            for i, student in enumerate(student_rankings):
                student['rank'] = i + 1
            
            # Time-based analysis
            interval_rankings = {}
            for item in class_timeline:
                interval = item['interval']
                if interval not in interval_rankings:
                    interval_rankings[interval] = []
                
                interval_rankings[interval].append({
                    "student_id": item['student_id'],
                    "student_name": item['student_name'],
                    "attention_rate": item['attention_rate'],
                    "status": item['status']
                })
            
            # Sort each interval by attention rate
            for interval in interval_rankings:
                interval_rankings[interval].sort(key=lambda x: x['attention_rate'], reverse=True)
                # Add ranks
                for i, student in enumerate(interval_rankings[interval]):
                    student['interval_rank'] = i + 1
            
            # Performance categories
            high_performers = [s for s in student_rankings if s['overall_attention_score'] >= 80]
            average_performers = [s for s in student_rankings if 60 <= s['overall_attention_score'] < 80]
            low_performers = [s for s in student_rankings if s['overall_attention_score'] < 60]
            
            return {
                "overall_ranking": student_rankings,
                "interval_rankings": interval_rankings,
                "performance_categories": {
                    "high_performers": {
                        "count": len(high_performers),
                        "students": high_performers,
                        "percentage": round((len(high_performers) / len(students_data)) * 100, 1) if students_data else 0
                    },
                    "average_performers": {
                        "count": len(average_performers),
                        "students": average_performers,
                        "percentage": round((len(average_performers) / len(students_data)) * 100, 1) if students_data else 0
                    },
                    "low_performers": {
                        "count": len(low_performers),
                        "students": low_performers,
                        "percentage": round((len(low_performers) / len(students_data)) * 100, 1) if students_data else 0
                    }
                },
                "class_insights": {
                    "most_consistent_student": self._find_most_consistent_student(students_data),
                    "most_improved_student": self._find_most_improved_student(students_data),
                    "needs_immediate_attention": [s['student_name'] for s in low_performers]
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating class rankings: {str(e)}")
            return {}

    def _find_most_consistent_student(self, students_data: list) -> dict:
        """Find the student with the most consistent attention."""
        try:
            best_consistency = -1
            most_consistent = None
            
            for student in students_data:
                intervals = student.get('time_intervals', [])
                scores = [interval.get('attention_rate', 0) for interval in intervals]
                consistency = self._calculate_consistency_score(scores)
                
                if consistency > best_consistency:
                    best_consistency = consistency
                    most_consistent = {
                        "student_id": student['student_id'],
                        "student_name": student['name'],
                        "consistency_score": consistency,
                        "overall_attention": student['overall_attention_score']
                    }
            
            return most_consistent or {}
            
        except Exception as e:
            self.logger.error(f"Error finding most consistent student: {str(e)}")
            return {}

    def _find_most_improved_student(self, students_data: list) -> dict:
        """Find the student who improved the most during the session."""
        try:
            best_improvement = -float('inf')
            most_improved = None
            
            for student in students_data:
                intervals = student.get('time_intervals', [])
                if len(intervals) < 2:
                    continue
                    
                scores = [interval.get('attention_rate', 0) for interval in intervals]
                improvement = scores[-1] - scores[0]  # Last - First
                
                if improvement > best_improvement:
                    best_improvement = improvement
                    most_improved = {
                        "student_id": student['student_id'],
                        "student_name": student['name'],
                        "improvement_percentage": round(improvement, 1),
                        "starting_attention": scores[0],
                        "ending_attention": scores[-1],
                        "overall_attention": student['overall_attention_score']
                    }
            
            return most_improved or {}
            
        except Exception as e:
            self.logger.error(f"Error finding most improved student: {str(e)}")
            return {}
            

    def _parse_ai_report_to_sections(self, raw_report: str) -> dict:
        """
        Parse the raw AI report into structured sections with multilingual support.
        """
        try:
            sections = {}
            lines = raw_report.split('\n')
            current_section = None
            current_content = []
            
            # Define multilingual section keywords
            section_keywords = {
                'executive_summary': [
                    'EXECUTIVE SUMMARY', 'YÖNETİCİ ÖZETİ', 'الملخص التنفيذي', 'RESUMEN EJECUTIVO',
                    'RÉSUMÉ EXÉCUTIF', 'ZUSAMMENFASSUNG', 'RIASSUNTO ESECUTIVO', 'RESUMO EXECUTIVO',
                    '执行摘要', 'エグゼクティブサマリー', 'РЕЗЮМЕ'
                ],
                'individual_analysis': [
                    'INDIVIDUAL STUDENT ANALYSIS', 'BİREYSEL ÖĞRENCİ ANALİZİ', 'تحليل الطلاب الفردي',
                    'ANÁLISIS INDIVIDUAL DE ESTUDIANTES', 'ANALYSE INDIVIDUELLE DES ÉTUDIANTS',
                    'INDIVIDUELLE STUDENTENANALYSE', 'ANALISI INDIVIDUALE DEGLI STUDENTI',
                    'ANÁLISE INDIVIDUAL DE ESTUDANTES', '个人学生分析', '個別学生分析',
                    'ИНДИВИДУАЛЬНЫЙ АНАЛИЗ СТУДЕНТОВ'
                ],
                'temporal_analysis': [
                    'TEMPORAL ANALYSIS', 'ZAMANSAL ANALİZ', 'التحليل الزمني', 'ANÁLISIS TEMPORAL',
                    'ANALYSE TEMPORELLE', 'ZEITANALYSE', 'ANALISI TEMPORALE', 'ANÁLISE TEMPORAL',
                    '时间分析', '時間分析', 'ВРЕМЕННОЙ АНАЛИЗ'
                ],
                'classroom_dynamics': [
                    'CLASSROOM DYNAMICS', 'SINIF DİNAMİKLERİ', 'ديناميكيات الفصل', 'DINÁMICAS DEL AULA',
                    'DYNAMIQUES DE CLASSE', 'KLASSENDYNAMIK', 'DINAMICHE DELLA CLASSE',
                    'DINÂMICAS DA SALA DE AULA', '课堂动态', '教室の動態', 'КЛАССНАЯ ДИНАМИКА'
                ],
                'recommendations': [
                    'ACTIONABLE RECOMMENDATIONS', 'UYGULANABİLİR ÖNERİLER', 'التوصيات القابلة للتنفيذ',
                    'RECOMENDACIONES ACCIONABLES', 'RECOMMANDATIONS PRATIQUES', 'UMSETZBARE EMPFEHLUNGEN',
                    'RACCOMANDAZIONI ATTUABILI', 'RECOMENDAÇÕES ACIONÁVEIS', '可行建议',
                    '実行可能な推奨事項', 'ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ'
                ],
                'metrics_summary': [
                    'METRICS SUMMARY', 'METRİK ÖZETİ', 'ملخص المقاييس', 'RESUMEN DE MÉTRICAS',
                    'RÉSUMÉ DES MÉTRIQUES', 'METRIKEN-ZUSAMMENFASSUNG', 'RIASSUNTO DELLE METRICHE',
                    'RESUMO DAS MÉTRICAS', '指标摘要', '指標要約', 'СВОДКА ПОКАЗАТЕЛЕЙ'
                ]
            }
            
            for line in lines:
                line_clean = line.strip()
                line_upper = line_clean.upper()
                
                # Check if this line is a section header
                found_section = None
                if line_clean.startswith('') and any(char.isdigit() for char in line_clean[:10]):
                    # Try to match against known section keywords
                    for section_key, keywords in section_keywords.items():
                        for keyword in keywords:
                            if keyword in line_upper:
                                found_section = section_key
                                break
                        if found_section:
                            break
                
                if found_section:
                    # Save previous section
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = found_section
                    current_content = []
                elif current_section and line_clean and not line_clean.startswith(''):
                    # Add content to current section
                    current_content.append(line)
            
            # Save the last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Ensure all sections exist with proper defaults
            default_sections = {
                'executive_summary': 'Not available',
                'individual_analysis': 'Not available', 
                'temporal_analysis': 'Not available',
                'classroom_dynamics': 'Not available',
                'recommendations': 'Not available',
                'metrics_summary': 'Not available'
            }
            
            for key, default_value in default_sections.items():
                if key not in sections or not sections[key].strip():
                    sections[key] = default_value
            
            # Debug log
            self.logger.info(f"Parsed {len(sections)} sections: {list(sections.keys())}")
            
            return sections
            
        except Exception as e:
            self.logger.error(f"Error parsing AI report: {str(e)}")
            return {
                'executive_summary': raw_report,
                'individual_analysis': 'Parsing error - see executive summary',
                'temporal_analysis': 'Parsing error - see executive summary', 
                'classroom_dynamics': 'Parsing error - see executive summary',
                'recommendations': 'Parsing error - see executive summary',
                'metrics_summary': 'Parsing error - see executive summary'
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
    import argparse
    
    parser = argparse.ArgumentParser(description='EduVision Classroom Report Processor')
    parser.add_argument('--csv_path', type=str, help='Path to the CSV file to process')
    parser.add_argument('--course_name', type=str, required=True, help='Name of the course (e.g., "Mathematics 101", "Physics Advanced")')  # Made required
    parser.add_argument('--language', type=str, default='en', help='Report language (english, Turkish, french, arabic, etc.)')
    
    args = parser.parse_args()
    
    print("🚀 EduVision Classroom Report Processor")
    print("="*60)
    
    processor = EduVisionClassroomProcessor()
    
    # Get CSV file path
    csv_file_path = args.csv_path
    course_name = args.course_name
    report_language = args.language.lower()
    
    if not csv_file_path:
        print("❌ No CSV file path provided. Use --csv_path to specify the file.")
        return
    
    try:
        # Test Gemini connection first
        print("\n🔍 Testing Gemini API connection...")
        if not processor.gemini_generator.test_connection():
            print("❌ Failed to connect to Gemini API. Check your API key in config.py")
            return
        
        print("✅ Gemini API connection successful!")
        print(f"📚 Course: {course_name}")  
        print(f"🌍 Language: {report_language.title()}")
        
        # Validate CSV format first
        print(f"\n📊 Validating CSV format...")
        validation = processor.csv_loader.validate_csv_format(csv_file_path)
        
        if not validation['valid']:
            print(f"❌ CSV validation failed: {validation.get('error', 'Invalid format')}")
            return
        
        print(f"✅ CSV valid: {validation['total_rows']} rows, {len(validation['available_optional_columns'])} optional columns")
        
        # Process the CSV
        print(f"\n⚡ Processing classroom reports...")
        results = processor.process_csv_file(csv_file_path,
                                            language=report_language,
                                            course_name=course_name,
                                            save_reports=True)
        
        # Display results
        print(f"\n📊 PROCESSING COMPLETE:")
        print(f"📚 Course: {course_name}")
        print(f"✅ Successful Classrooms: {results['successful_reports']}")
        print(f"❌ Failed Classrooms: {results['failed_reports']}")
        print(f"👥 Total Students: {results['total_students']}")
        print(f"📁 Reports saved in 'reports/' directory")
        print(f"🌍 Using language: '{report_language}'")
        
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