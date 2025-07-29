import re 
from datetime import datetime
from typing import Dict, List, Optional

class ReportFormatter:
    """
    A helper module to clean, structure, and reformat AI-generated reports.
    """
    
    def __init__(self):
        """
        Initialize the formatter with default settings.
        """
        self.section_headers = [
            "PERFORMANCE REPORT",
            "PERFORMANCE SUMMARY", 
            "RECOMMENDATIONS",
            "ACTIONABLE RECOMMENDATIONS",
            "PATTERN ANALYSIS",
            "CONCERNING PATTERNS",
            "INTERVENTION URGENCY",
            "URGENCY RATING"
        ]

    def format_report(self, raw_report: str, student_name: str, student_id: str) -> Dict[str, str]:
        """
        Clean and structure the raw AI-generated report.

        Args:
            raw_report (str): Raw text from Gemini API
            student_name (str): student's name
            student_id (str): student's ID

        Returns:
            Dict[str, str]: Structured report with separate sections.
        """

        # Clean the raw text 
        cleaned_text = self._clean_text(raw_report)

        # Extract sections
        sections = self._extract_sections(cleaned_text)

        # Format each section
        formatted_report = {
            "student_name": student_name,
            "student_id": student_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "performance_summary": self._format_performance_section(sections.get('performance', '')),
            "recommendations": self._format_recommendations_section(sections.get('recommendations', '')),
            "pattern_analysis": self._format_pattern_section(sections.get('patterns', '')),
            "urgency_rating": self._format_urgency_section(sections.get('urgency', '')),
            "full_report": self._create_full_formatted_report(sections, student_name, student_id)
        }

        return formatted_report
    
    def _clean_text(self, text: str) -> str:
        """
        Remove unwanted characters and normalize spacing.
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove markdown formatting that might interfere
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Remove **bold**
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Remove *italic*

        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Clean up multiple line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract different sections from the report text.
        """
        sections = {}

        # Improved section patterns
        patterns = {
            'performance': [
                r'(?:##\s*PERFORMANCE\s+(?:REPORT|SUMMARY))[\s:]*\n*(.*?)(?=(?:##\s*RECOMMENDATIONS|##\s*PATTERN|##\s*INTERVENTION|$))',
                r'(?:PERFORMANCE\s+(?:REPORT|SUMMARY))[\s:]*\n*(.*?)(?=(?:RECOMMENDATIONS|PATTERN|URGENCY|$))'
            ],
            'recommendations': [
                r'(?:##\s*(?:ACTIONABLE\s+)?RECOMMENDATIONS)[\s:]*\n*(.*?)(?=(?:##\s*PATTERN|##\s*INTERVENTION|$))',
                r'(?:(?:ACTIONABLE\s+)?RECOMMENDATIONS)[\s:]*\n*(.*?)(?=(?:PATTERN|URGENCY|$))'
            ],
            'patterns': [
                r'(?:##\s*PATTERN\s+ANALYSIS)[\s:]*\n*(.*?)(?=(?:##\s*INTERVENTION|$))',
                r'(?:PATTERN\s+ANALYSIS|CONCERNING\s+PATTERNS)[\s:]*\n*(.*?)(?=(?:URGENCY|$))'
            ],
            'urgency': [
                r'(?:##\s*INTERVENTION\s+URGENCY)[\s:]*\n*(.*?)$',
                r'(?:INTERVENTION\s+URGENCY|URGENCY\s+RATING)[\s:]*\n*(.*?)$'
            ]
        }
        
        for section_name, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    sections[section_name] = match.group(1).strip()
                    break

        return sections
    
    def _format_performance_section(self, text: str) -> str:
        """
        Format the performance summary section.
        """
        if not text:
            return "Performance summary not available."
        
        # Clean and format
        text = self._clean_text(text)
        
        # Ensure it ends with proper punctuation
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text

    def _format_recommendations_section(self, text: str) -> List[str]:
        """
        Format the recommendations into a structured List.
        """
        if not text:
            return ["No recommendations provided."]
        
        # Extract bullet points or numbered items
        recommendations = []

        # Split by lines and process
        lines = text.split("\n")
        current_rec = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's a new recommendation (starts with bullet, number, or dash)
            if re.match(r'^[\-\*\•]\s*', line) or re.match(r'^\d+\.?\s*', line):
                # Save previous recommendation if exists
                if current_rec:
                    recommendations.append(self._clean_recommendation(current_rec))
                # Start new recommendation, removing the bullet/number
                current_rec = re.sub(r'^[\-\*\•\d\.]\s*', '', line)
            else:
                # Continue current recommendation
                if current_rec:
                    current_rec += " " + line
                else:
                    current_rec = line

        # Add the last recommendation
        if current_rec:
            recommendations.append(self._clean_recommendation(current_rec))

        # If still no structured recommendations, try splitting by common separators
        if not recommendations or len(recommendations) == 1:
            # Try splitting by common patterns like "- Long-term:", "Parent involvement:", etc.
            parts = re.split(r'\s*-\s*(?:Immediate|Long-term|Parent|Home|Classroom)', text)
            if len(parts) > 1:
                recommendations = []
                for i, part in enumerate(parts[1:], 1):  # Skip first empty part
                    clean_part = part.strip().rstrip(':').strip()
                    if clean_part:
                        recommendations.append(self._clean_recommendation(clean_part))
        
        # Final fallback: split by sentences
        if not recommendations:
            sentences = re.split(r'[.!?]+', text)
            recommendations = [self._clean_recommendation(s.strip()) for s in sentences if s.strip()]
        
        return recommendations[:3]  # Limit to 3 recommendations as requested

    def _clean_recommendation(self, rec: str) -> str:
        """
        Clean individual recommendation text.
        """
        rec = rec.strip()

        # Remove category prefixes like "Immediate:", "Long-term:", etc.
        rec = re.sub(r'^(?:Immediate|Long-term|Home|Parent|Classroom)\s*(?:strategy|intervention|involvement)?\s*:?\s*', '', rec, flags=re.IGNORECASE)

        # Remove leading dashes or bullets that might remain
        rec = re.sub(r'^[\-\*\•\s]*', '', rec)

        # Ensure proper capitalization
        if rec:
            rec = rec[0].upper() + rec[1:] if len(rec) > 1 else rec.upper()
        
        # Ensure proper punctuation
        if rec and not rec.endswith(('.', '!', '?')):
            rec += '.'
        
        return rec

    def _format_pattern_section(self, text: str) -> str:
        """
        Format the pattern analysis section.
        """
        if not text:
            return "No concerning patterns identified."
        
        text = self._clean_text(text)
        
        # Remove any stray section headers that might have been captured
        text = re.sub(r'^(?:ANALYSIS|PATTERN\s+ANALYSIS)[\s:]*', '', text, flags=re.IGNORECASE)
        
        # Ensure proper punctuation
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def _format_urgency_section(self, text: str) -> Dict[str, str]:
        """Extract urgency level and explanation."""
        if not text:
            return {"level": "Unknown", "explanation": "Urgency level not specified."}
        
        text = self._clean_text(text)
        
        # Extract urgency level
        urgency_match = re.search(r'\b(Low|Medium|High)\b', text, re.IGNORECASE)
        urgency_level = urgency_match.group(1).title() if urgency_match else "Unknown"
        
        # Extract explanation (text after the urgency level)
        if urgency_match:
            explanation = text[urgency_match.end():].strip()
            explanation = re.sub(r'^[\s\-:]+', '', explanation)  # Remove leading punctuation
        else:
            explanation = text
        
        if explanation and not explanation.endswith(('.', '!', '?')):
            explanation += '.'
        
        return {
            "level": urgency_level,
            "explanation": explanation or "No explanation provided."
        }
    
    def _create_full_formatted_report(self, sections: Dict[str, str], student_name: str, student_id: str) -> str:
        """Create a nicely formatted full report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
STUDENT FOCUS REPORT
{'='*50}
Student: {student_name} (ID: {student_id})
Generated: {timestamp}

PERFORMANCE SUMMARY
{'-'*30}
{self._format_performance_section(sections.get('performance', ''))}

RECOMMENDATIONS
{'-'*30}
"""
        
        recommendations = self._format_recommendations_section(sections.get('recommendations', ''))
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        urgency = self._format_urgency_section(sections.get('urgency', ''))
        
        report += f"""
PATTERN ANALYSIS
{'-'*30}
{self._format_pattern_section(sections.get('patterns', ''))}

INTERVENTION URGENCY
{'-'*30}
Level: {urgency['level']}
Explanation: {urgency['explanation']}
"""
        
        return report.strip()
    
    def save_formatted_report(self, formatted_report: Dict[str, str], filename: str, output_dir: str = "reports") -> bool:
        """Save the formatted report to a file."""
        try:
            import os
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(formatted_report['full_report'])
            
            return True
        except Exception:
            return False

# Quick test
if __name__ == "__main__":
    # Test the formatter
    raw_sample = """
    ## PERFORMANCE REPORT
    John shows moderate attention levels during the session with some concerning patterns.
    
    ## RECOMMENDATIONS
    - Immediate: Seat student closer to teacher
    - Long-term: Implement focus breaks every 15 minutes  
    - Parent involvement: Ensure adequate sleep schedule
    
    ## PATTERN ANALYSIS
    Student shows decreased focus in afternoon sessions.
    
    ## INTERVENTION URGENCY
    Medium - Some attention issues but manageable with proper strategies.
    """
    
    formatter = ReportFormatter()
    result = formatter.format_report(raw_sample, "John Doe", "STU001")
    
    print("FORMATTED REPORT:")
    print(result['full_report'])
    print("\nINDIVIDUAL SECTIONS:")
    print("Performance:", result['performance_summary'])
    print("Recommendations:", result['recommendations'])
    print("Patterns:", result['pattern_analysis'])
    print("Urgency:", result['urgency_rating'])