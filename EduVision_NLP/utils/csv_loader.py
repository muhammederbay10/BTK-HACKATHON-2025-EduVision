import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

class CSVLoader:
    """Handles loading and processing of CSV data from computer vision models."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.required_columns = [
            'student_id', 'timestamp', 'attention_status', 
            'attention_score', 'distraction_events'
        ]
        self.optional_columns = [
            'course_name', 'name', 'gaze', 'yaw_angle_deg', 
            'yawning_count', 'eye_closure_duration_sec', 
            'focus_quality', 'session_duration_minutes'
        ]
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """Load CSV file and return DataFrame."""
        try:
            df = pd.read_csv(file_path)
            self.logger.info(f"Loaded CSV with {len(df)} records from {file_path}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV: {str(e)}")
            raise
    
    def validate_csv_format(self, file_path: str) -> dict:
        """Validate CSV format and return validation results."""
        try:
            df = pd.read_csv(file_path)
            
            # Check required columns
            missing_required = [col for col in self.required_columns if col not in df.columns]
            if missing_required:
                return {
                    'valid': False,
                    'error': f"Missing required columns: {missing_required}"
                }
            
            # Check optional columns
            available_optional = [col for col in self.optional_columns if col in df.columns]
            
            return {
                'valid': True,
                'total_rows': len(df),
                'available_optional_columns': available_optional
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def _aggregate_student_data(self, student_df: pd.DataFrame, interval_minutes: int = 3) -> list:
        """Aggregate frame-level data into time intervals."""
        try:
            # Convert timestamp to datetime
            student_df['timestamp'] = pd.to_datetime(student_df['timestamp'])
            
            # Sort by timestamp
            student_df = student_df.sort_values('timestamp')
            
            # Calculate total session duration in minutes
            start_time = student_df['timestamp'].min()
            end_time = student_df['timestamp'].max()
            total_duration = (end_time - start_time).total_seconds() / 60
            
            # Create time intervals
            intervals = []
            current_time = start_time
            
            while current_time < end_time:
                interval_end = current_time + timedelta(minutes=interval_minutes)
                
                # Filter data for this interval
                interval_data = student_df[
                    (student_df['timestamp'] >= current_time) & 
                    (student_df['timestamp'] < interval_end)
                ]
                
                if len(interval_data) > 0:
                    # Aggregate the interval data
                    aggregated = {
                        'interval_start': current_time.strftime('%H:%M:%S'),
                        'interval_duration_minutes': interval_minutes,
                        'avg_attention_score': interval_data['attention_score'].mean(),
                        'attention_rate': (interval_data['attention_status'] == 'Attentive').mean() * 100,
                        'total_distractions': interval_data['distraction_events'].max() - interval_data['distraction_events'].min(),
                        'frames_analyzed': len(interval_data)
                    }
                    
                    # Add optional fields if available
                    if 'yawning_count' in interval_data.columns:
                        aggregated['yawning_incidents'] = interval_data['yawning_count'].max()
                    
                    if 'eye_closure_duration_sec' in interval_data.columns:
                        aggregated['avg_eye_closure'] = interval_data['eye_closure_duration_sec'].mean()
                    
                    # Determine overall attention for this interval
                    if aggregated['attention_rate'] >= 70:
                        aggregated['interval_status'] = 'Highly Attentive'
                    elif aggregated['attention_rate'] >= 50:
                        aggregated['interval_status'] = 'Moderately Attentive'
                    else:
                        aggregated['interval_status'] = 'Needs Attention'
                    
                    intervals.append(aggregated)
                
                current_time = interval_end
            
            return intervals, total_duration
            
        except Exception as e:
            self.logger.error(f"Error aggregating student data: {str(e)}")
            return [], 0
    
    def get_student_data(self, df: pd.DataFrame) -> list:
        """Process and return structured student data with time aggregation."""
        try:
            # Clean data first
            df_clean = self._clean_data(df)
            
            students_data = []
            unique_students = df_clean['student_id'].unique()
            
            for student_id in unique_students:
                student_df = df_clean[df_clean['student_id'] == student_id].copy()
                
                if len(student_df) == 0:
                    continue
                
                # Aggregate data into 3-minute intervals
                intervals, total_duration = self._aggregate_student_data(student_df, interval_minutes=3)
                
                if not intervals:
                    continue
                
                # Calculate overall session statistics
                overall_attention = np.mean([interval['attention_rate'] for interval in intervals])
                total_distractions = sum([interval['total_distractions'] for interval in intervals])
                
                student_data = {
                    'student_id': student_id,
                    'name': student_df.get('name', f"Student {student_id}").iloc[0] if 'name' in student_df.columns else f"Student {student_id[:8]}",
                    'course_name': student_df.get('course_name', 'Unknown Course').iloc[0] if 'course_name' in student_df.columns else 'Unknown Course',
                    'session_time': student_df['timestamp'].iloc[0] if 'timestamp' in student_df.columns else 'Unknown',
                    'total_session_minutes': round(total_duration, 1),
                    'overall_attention_score': round(overall_attention, 1),
                    'total_distractions': int(total_distractions),
                    'intervals_analyzed': len(intervals),
                    'time_intervals': intervals
                }
                
                students_data.append(student_data)
            
            self.logger.info(f"Successfully processed {len(students_data)} students with time aggregation")
            return students_data
            
        except Exception as e:
            self.logger.error(f"Error processing student data: {str(e)}")
            raise
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the data."""
        initial_count = len(df)
        
        # Remove rows with missing required data
        df_clean = df.dropna(subset=['student_id', 'attention_status', 'attention_score'])
        
        # Remove duplicate records (same student, same timestamp)
        if 'timestamp' in df_clean.columns:
            df_clean = df_clean.drop_duplicates(subset=['student_id', 'timestamp'])
        
        # Validate attention_score range
        df_clean = df_clean[
            (df_clean['attention_score'] >= 0) & 
            (df_clean['attention_score'] <= 100)
        ]
        
        removed_count = initial_count - len(df_clean)
        if removed_count > 0:
            self.logger.warning(f"Removed {removed_count} invalid/duplicate records")
        
        self.logger.info(f"Successfully validated {len(df_clean)} records")
        return df_clean
    
    def get_summary_stats(self, df: pd.DataFrame) -> dict:
        """Generate summary statistics from the DataFrame."""
        try:
            df_clean = self._clean_data(df)
            students_data = self.get_student_data(df_clean)
            
            if not students_data:
                return {'error': 'No valid student data found'}
            
            # Calculate statistics from aggregated data
            total_students = len(students_data)
            unique_courses = len(set([s['course_name'] for s in students_data]))
            
            course_breakdown = {}
            for student in students_data:
                course = student['course_name']
                course_breakdown[course] = course_breakdown.get(course, 0) + 1
            
            avg_attention = np.mean([s['overall_attention_score'] for s in students_data])
            avg_distractions = np.mean([s['total_distractions'] for s in students_data])
            avg_session_length = np.mean([s['total_session_minutes'] for s in students_data])
            
            # Categorize students
            students_needing_support = sum(1 for s in students_data if s['overall_attention_score'] < 60)
            high_performers = sum(1 for s in students_data if s['overall_attention_score'] >= 80)
            
            return {
                'total_students': total_students,
                'unique_courses': unique_courses,
                'course_breakdown': course_breakdown,
                'avg_attention_score': round(avg_attention, 1),
                'avg_distractions': round(avg_distractions, 1),
                'avg_session_length': round(avg_session_length, 1),
                'students_needing_support': students_needing_support,
                'high_performers': high_performers
            }
            
        except Exception as e:
            self.logger.error(f"Error generating summary stats: {str(e)}")
            return {'error': str(e)}
    
    def get_classroom_batches(self, df: pd.DataFrame) -> dict:
        """Group students by classroom/course and return processed data."""
        try:
            students_data = self.get_student_data(df)
            
            classroom_batches = {}
            for student in students_data:
                course_name = student['course_name']
                if course_name not in classroom_batches:
                    classroom_batches[course_name] = []
                classroom_batches[course_name].append(student)
            
            return classroom_batches
            
        except Exception as e:
            self.logger.error(f"Error creating classroom batches: {str(e)}")
            return {}
    
    def apply_course_name(self, df: pd.DataFrame, course_name: str) -> pd.DataFrame:
        """Apply course name to all records in the DataFrame."""
        try:
            df_copy = df.copy()
            df_copy['course_name'] = course_name
            self.logger.info(f"Applied course name '{course_name}' to all {len(df_copy)} students")
            return df_copy
        except Exception as e:
            self.logger.error(f"Error applying course name: {str(e)}")
            raise
    
