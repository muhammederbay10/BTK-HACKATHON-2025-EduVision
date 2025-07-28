def build_prompt(student_name, Student_id, course_name, student_data):
    """
    Build a prompt for generating a report based on student data.

    Args:
        student_name (str): The name of the student.
        Student_id (str): The ID of the student.
        course_name (str): The name of the course.
        student_data (dict): A dictionary containing various data about the student.

    Returns:
        str: A formatted prompt string for generating a report.    
    """
    prompt = f"Generate a report for the following student:\n"
    prompt += f"Name: {student_name}\n"
    prompt += f"ID: {Student_id}\n"
    prompt += f"Course: {course_name}\n"
    attention_level = _classify_attension_level(student_data['metrics']["attension_score"])
    distraction_rate = _classify_distraction_rate(
        student_data['metrics']["distraction_events"],
        student_data['metrics']["total_session_minutes"])
    focus_quality = _classify_focus_quality(student_data['metrics'])
 
    
    return prompt, f"""
You are an AI assistant helping teachers monitor student focus and engagement.

Here is {student_data['name']}'s behavior data from today's session:

ATTENTION METRICS:
- Overall Attention Score: {student_data['metrics']['attention_score']}% ({attention_level})
- Distraction Events: {student_data['metrics']['distraction_events']} ({distraction_rate:.1f} per minute)
- Yawning Count: {student_data['metrics']['yawning_count']}
- Eye Closure Duration: {student_data['metrics']['eye_closure_duration_sec']} seconds
- Session Duration: {student_data['metrics']['total_session_minutes']} minutes
- Focus Quality Assessment: {focus_quality}

ADDITIONAL CONTEXT:
- Time of Day: {student_data.get('session_time', 'Not specified')}
- Subject/Activity: {student_data.get('subject', 'General classroom activity')}
- Previous Session Comparison: {student_data.get('trend', 'No previous data')}

TASK:
1. Write a clear, professional performance report (3-4 sentences) that a teacher can easily understand and share with parents if needed.

2. Provide 3 specific, actionable recommendations:
   - One immediate classroom strategy
   - One longer-term intervention
   - One suggestion for home/parent involvement

3. Identify any concerning patterns that might need further attention.

4. Rate the urgency of intervention needed (Low/Medium/High) and explain why.

Format your response clearly with headers for each section.
"""

def _classify_attension_level(attention_score: float) -> str:
    """
    Classify the attention level based on the attention score.
    """
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
    """
    Calculate the distraction rate per minute.
    """
    if total_session_minutes == 0:
        return 0.0
    return distraction_events / total_session_minutes

def _classify_focus_quality(metrics: dict) -> str:
    """
    Assess overall focus quality based on multiple metrics.
    """
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
