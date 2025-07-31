def build_classroom_prompt(students_data: list, class_info: dict) -> str:
    """Build a comprehensive classroom attention analysis prompt."""
    
    prompt = f"""
You are an expert educational analyst specializing in classroom attention and engagement patterns. 
Analyze the following classroom session data and provide a comprehensive report.

CLASSROOM INFORMATION:
- Course: {class_info.get('course_name', 'Unknown')}
- Session Date: {class_info.get('date', 'Unknown')}
- Session Time: {class_info.get('session_time', 'Unknown')}
- Total Students: {len(students_data)}

STUDENT ATTENTION DATA (Aggregated in 3-minute intervals):
"""
    
    for i, student in enumerate(students_data, 1):
        prompt += f"""
STUDENT {i}:
- ID: {student['student_id']}
- Name: {student['name']}
- Total Session Duration: {student['total_session_minutes']} minutes
- Overall Attention Score: {student['overall_attention_score']}%
- Total Distractions: {student['total_distractions']}
- Intervals Analyzed: {student['intervals_analyzed']}

TIME INTERVAL BREAKDOWN:
"""
        for interval in student['time_intervals']:
            prompt += f"  • {interval['interval_start']} ({interval['interval_duration_minutes']}min): "
            prompt += f"{interval['interval_status']} - {interval['attention_rate']:.1f}% attention, "
            prompt += f"{interval['total_distractions']} distractions\n"
    
    prompt += f"""

ANALYSIS REQUIREMENTS:
Please provide a detailed classroom report with the following sections:

1. EXECUTIVE SUMMARY
   - Overall classroom engagement level
   - Key findings and trends
   - Critical attention patterns

2. INDIVIDUAL STUDENT ANALYSIS
   - Performance summary for each student
   - Attention patterns throughout the session
   - Students requiring additional support

3. TEMPORAL ANALYSIS
   - How attention levels changed during the session
   - Peak engagement periods
   - Times when attention dropped

4. CLASSROOM DYNAMICS
   - Overall class engagement trends
   - Comparison between high and low performers
   - Collective attention patterns

5. ACTIONABLE RECOMMENDATIONS
   - Specific strategies for improving engagement
   - Individual student interventions needed
   - Optimal timing for key content delivery
   - Environmental or teaching method adjustments

6. METRICS SUMMARY
   - Average class attention score
   - Range of student performance
   - Distraction frequency analysis

Format your response as a professional educational report suitable for teachers and administrators.
Use clear headings and bullet points for easy reading.
"""
    
    return prompt