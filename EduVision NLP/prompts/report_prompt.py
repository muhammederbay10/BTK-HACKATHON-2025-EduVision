def build_classroom_prompt(students_data: list, class_info: dict) -> str:
    """
    Build a prompt for generating a classroom-wide report based on multiple students' data.

    Args:
        students_data (list): List of student data dictionaries
        class_info (dict): Information about the class (course_name, session_time, etc.)

    Returns:
        str: A formatted prompt string for generating a classroom report.    
    """
    
    # Analyze the class data
    total_students = len(students_data)
    attention_scores = [student['metrics']['attention_score'] for student in students_data]
    avg_attention = sum(attention_scores) / total_students
    
    # Classify students by performance using IDs
    high_performers = []
    medium_performers = []
    low_performers = []
    
    for student in students_data:
        score = student['metrics']['attention_score']
        student_id = student['student_id']
        if score >= 75:
            high_performers.append(f"ID-{student_id} ({score:.1f}%)")
        elif score >= 50:
            medium_performers.append(f"ID-{student_id} ({score:.1f}%)")
        else:
            low_performers.append(f"ID-{student_id} ({score:.1f}%)")
    
    # Analyze time-based distraction patterns
    time_analysis = _analyze_time_based_distractions(students_data)
    
    # Get class statistics
    class_stats = _get_class_statistics(students_data)
    
    # Build the prompt
    prompt = f"""
You are an AI assistant helping teachers analyze classroom-wide focus and engagement patterns.

CLASS INFORMATION:
- Course: {class_info.get('course_name', 'Not specified')}
- Session Time: {class_info.get('session_time', 'Not specified')}
- Date: {class_info.get('date', 'Today')}
- Total Students: {total_students}

CLASSROOM ATTENTION ANALYSIS:
- Average Class Attention Score: {avg_attention:.1f}%
- High Performers ({len(high_performers)} students): {', '.join(high_performers[:8])}
- Medium Performers ({len(medium_performers)} students): {', '.join(medium_performers[:5])}
- Students Needing Support ({len(low_performers)} students): {', '.join(low_performers)}

CLASS STATISTICS:
- Average Distraction Events per Student: {class_stats['avg_distractions']:.1f}
- Total Yawning Incidents: {class_stats['total_yawns']}
- Students with High Distraction (>10 events): {len(class_stats['high_distraction_students'])} students
- Most Alert Period: {class_stats['peak_attention_time']}

TIME-BASED DISTRACTION ANALYSIS:
{time_analysis['summary']}

PEAK DISTRACTION PERIODS:
"""

    # Add time-based distraction details
    for period in time_analysis['peak_periods']:
        prompt += f"- Minutes {period['start_min']}-{period['end_min']}: {len(period['affected_students'])} students distracted\n"
        prompt += f"  Affected Student IDs: {', '.join(period['affected_students'])}\n"
        prompt += f"  Distraction Rate: {period['distraction_rate']:.1f} events/minute\n"

    prompt += f"""

DETAILED STUDENT DATA:
"""

    # Add individual student summaries using IDs
    for student in students_data:
        attention_level = _classify_attention_level(student['metrics']['attention_score'])
        distraction_rate = _classify_distraction_rate(
            student['metrics']['distraction_events'],
            student['metrics']['total_session_minutes']
        )
        
        prompt += f"- Student ID-{student['student_id']}: {student['metrics']['attention_score']:.1f}% attention ({attention_level}), "
        prompt += f"{student['metrics']['distraction_events']} distractions ({distraction_rate:.1f}/min), "
        prompt += f"{student['metrics']['yawning_count']} yawns\n"

    prompt += f"""

YOUR TASK:
Generate a comprehensive classroom focus report that includes:

## CLASSROOM OVERVIEW
Provide a 3-4 sentence summary of the overall classroom attention and engagement during this session.

## PERFORMANCE HIGHLIGHTS
- Recognize the top-performing student IDs and their achievements
- Identify student IDs who need additional support
- Note any patterns across different performance levels

## TIME-BASED RECOMMENDATIONS
Based on the peak distraction periods identified:
- Explain what might have caused distractions during specific time periods
- Provide strategies to prevent future distractions during these critical minutes
- Suggest optimal timing for breaks, difficult material, or activity changes

## TARGETED STUDENT INTERVENTIONS
For each distraction period, provide specific recommendations:
- Which student IDs need immediate attention
- What type of intervention would be most effective
- How to prevent similar patterns in future sessions

## CLASSROOM MANAGEMENT STRATEGIES
Provide 4 specific, actionable recommendations:
1. **Immediate Response Protocol**: How to handle peak distraction periods in real-time
2. **Preventive Measures**: Environmental or instructional changes to reduce distractions
3. **Individual Student Support**: Specific guidance for the most distracted student IDs
4. **Session Structure Optimization**: How to restructure the class based on attention patterns

## INTERVENTION PRIORITY
- **High Priority Student IDs**: Students needing immediate intervention
- **Medium Priority Student IDs**: Students requiring monitoring
- **Peak Distraction Times**: Time periods that need special attention
- Overall class focus assessment and urgency level

Format your response with clear headers and reference specific student IDs throughout the report.
"""
    
    return prompt

def _analyze_time_based_distractions(students_data: list) -> dict:
    """
    Analyze distraction patterns across time periods.
    
    Args:
        students_data (list): List of student data dictionaries
        
    Returns:
        dict: Time-based analysis results
    """
    # For now, we'll simulate time-based analysis
    # In real implementation, you'd get this from your computer vision model
    
    total_session_minutes = students_data[0]['metrics']['total_session_minutes'] if students_data else 30
    
    # Simulate peak distraction periods (this would come from your CV model)
    peak_periods = []
    
    # Example: Simulate that students got distracted in specific time windows
    # This should be replaced with actual time-stamped distraction data from CV model
    high_distraction_students = [
        s for s in students_data 
        if s['metrics']['distraction_events'] > 8
    ]
    
    if high_distraction_students:
        # Simulate distraction periods
        if len(high_distraction_students) >= 3:
            peak_periods.append({
                'start_min': 5,
                'end_min': 7,
                'affected_students': [f"ID-{s['student_id']}" for s in high_distraction_students[:4]],
                'distraction_rate': 2.5
            })
        
        if len(high_distraction_students) >= 2:
            peak_periods.append({
                'start_min': 18,
                'end_min': 22,
                'affected_students': [f"ID-{s['student_id']}" for s in high_distraction_students[:3]],
                'distraction_rate': 1.8
            })
    
    # Generate summary
    if peak_periods:
        summary = f"Identified {len(peak_periods)} peak distraction periods during the session."
    else:
        summary = "No significant peak distraction periods identified. Class maintained consistent focus."
    
    return {
        'peak_periods': peak_periods,
        'summary': summary,
        'total_periods': len(peak_periods)
    }

def _get_class_statistics(students_data: list) -> dict:
    """Calculate classroom-wide statistics using student IDs."""
    if not students_data:
        return {}
    
    total_distractions = sum(s['metrics']['distraction_events'] for s in students_data)
    total_yawns = sum(s['metrics']['yawning_count'] for s in students_data)
    avg_distractions = total_distractions / len(students_data)
    
    high_distraction_students = [
        f"ID-{s['student_id']}" for s in students_data 
        if s['metrics']['distraction_events'] > 10
    ]
    
    # Determine peak attention time (simplified)
    session_times = [s.get('session_time', '') for s in students_data]
    peak_time = max(set(session_times), key=session_times.count) if session_times else "Not determined"
    
    return {
        'avg_distractions': avg_distractions,
        'total_yawns': total_yawns,
        'high_distraction_students': high_distraction_students,
        'peak_attention_time': peak_time
    }

def _classify_attention_level(attention_score: float) -> str:
    """Classify the attention level based on the attention score."""
    if attention_score >= 80:
        return "Excellent"
    elif attention_score >= 65:
        return "Good"
    elif attention_score >= 50:
        return "Fair"
    elif attention_score >= 35:
        return "Poor"
    else:
        return "Very Poor"
    
def _classify_distraction_rate(distraction_events: int, total_session_minutes: int) -> float:
    """Calculate the distraction rate per minute."""
    if total_session_minutes == 0:
        return 0.0
    return distraction_events / total_session_minutes

def _classify_focus_quality(metrics: dict) -> str:
    """Assess overall focus quality based on multiple metrics."""
    attention_score = metrics["attention_score"]
    yawning_count = metrics["yawning_count"]
    eye_closure_duration = metrics["eye_closure_duration_sec"]
    session_minutes = metrics["total_session_minutes"]

    # Calculate quality indicators
    yawn_rate = yawning_count / session_minutes if session_minutes > 0 else 0
    eye_closure_percentage = (eye_closure_duration / (session_minutes * 60)) * 100 if session_minutes > 0 else 0

    if attention_score >= 75 and yawn_rate < 0.5 and eye_closure_percentage < 5:
        return "High - Student shows strong engagement and focus."
    elif attention_score >= 60 and (yawn_rate < 1 or eye_closure_percentage < 10):
        return "Medium - Student is generally focused but shows some signs of fatigue."
    elif attention_score >= 40 or (yawn_rate < 2 and eye_closure_percentage < 20):
        return "Low - Student is struggling to maintain focus and may need support."
    else:
        return "Very Low - Student is highly distracted and requires immediate intervention."

# Keep the old function for backward compatibility but update it to use classroom approach
def build_prompt(student_name, student_id, course_name, student_data):
    """Legacy function - now creates a single-student classroom report using ID."""
    # Add student_id to student_data if not present
    if 'student_id' not in student_data:
        student_data['student_id'] = student_id
    
    class_info = {'course_name': course_name}
    return build_classroom_prompt([student_data], class_info)