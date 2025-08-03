import re 
from datetime import datetime
from typing import Dict, List, Optional

class ReportFormatter:
    """
    A helper module to clean, structure, and reformat AI-generated reports.
    Updated for classroom-wide reports.
    """
    
    def __init__(self):
        """Initialize the formatter with updated section headers for classroom reports."""
        self.section_headers = [
            "CLASSROOM OVERVIEW",
            "PERFORMANCE HIGHLIGHTS", 
            "TIME-BASED RECOMMENDATIONS",
            "TARGETED STUDENT INTERVENTIONS",
            "CLASSROOM MANAGEMENT STRATEGIES",
            "INTERVENTION PRIORITY"
        ]

    def format_report(self, raw_report: str, class_name: str, class_id: str) -> Dict[str, str]:
        """
        Clean and structure the raw AI-generated classroom report.

        Args:
            raw_report (str): Raw text from Gemini API
            class_name (str): Name of the class/course
            class_id (str): Class identifier

        Returns:
            Dict[str, str]: Structured report with separate sections.
        """
        # Clean the raw text 
        cleaned_text = self._clean_text(raw_report)

        # Extract sections for classroom report
        sections = self._extract_classroom_sections(cleaned_text)

        # Format each section
        formatted_report = {
            "class_name": class_name,
            "class_id": class_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "classroom_overview": self._format_overview_section(sections.get('overview', '')),
            "performance_highlights": self._format_performance_highlights(sections.get('performance', '')),
            "time_recommendations": self._format_time_recommendations(sections.get('time_recommendations', '')),
            "student_interventions": self._format_student_interventions(sections.get('interventions', '')),
            "management_strategies": self._format_management_strategies(sections.get('strategies', '')),
            "intervention_priority": self._format_intervention_priority(sections.get('priority', '')),
            "full_report": self._create_full_classroom_report(sections, class_name, class_id)
        }

        return formatted_report
    
    def _clean_text(self, text: str) -> str:
        """Remove unwanted characters and normalize spacing."""
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
    
    def _extract_classroom_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from the classroom report text."""
        sections = {}

        # Updated patterns for classroom report sections
        patterns = {
            'overview': [
                r'(?:##\s*CLASSROOM\s+OVERVIEW)[\s:]*\n*(.*?)(?=(?:##\s*PERFORMANCE|##\s*TIME|$))',
                r'(?:CLASSROOM\s+OVERVIEW)[\s:]*\n*(.*?)(?=(?:PERFORMANCE|TIME|$))'
            ],
            'performance': [
                r'(?:##\s*PERFORMANCE\s+HIGHLIGHTS)[\s:]*\n*(.*?)(?=(?:##\s*TIME|##\s*TARGETED|$))',
                r'(?:PERFORMANCE\s+HIGHLIGHTS)[\s:]*\n*(.*?)(?=(?:TIME|TARGETED|$))'
            ],
            'time_recommendations': [
                r'(?:##\s*TIME-BASED\s+RECOMMENDATIONS)[\s:]*\n*(.*?)(?=(?:##\s*TARGETED|##\s*CLASSROOM\s+MANAGEMENT|$))',
                r'(?:TIME-BASED\s+RECOMMENDATIONS)[\s:]*\n*(.*?)(?=(?:TARGETED|CLASSROOM\s+MANAGEMENT|$))'
            ],
            'interventions': [
                r'(?:##\s*TARGETED\s+STUDENT\s+INTERVENTIONS)[\s:]*\n*(.*?)(?=(?:##\s*CLASSROOM\s+MANAGEMENT|##\s*INTERVENTION\s+PRIORITY|$))',
                r'(?:TARGETED\s+STUDENT\s+INTERVENTIONS)[\s:]*\n*(.*?)(?=(?:CLASSROOM\s+MANAGEMENT|INTERVENTION\s+PRIORITY|$))'
            ],
            'strategies': [
                r'(?:##\s*CLASSROOM\s+MANAGEMENT\s+STRATEGIES)[\s:]*\n*(.*?)(?=(?:##\s*INTERVENTION\s+PRIORITY|$))',
                r'(?:CLASSROOM\s+MANAGEMENT\s+STRATEGIES)[\s:]*\n*(.*?)(?=(?:INTERVENTION\s+PRIORITY|$))'
            ],
            'priority': [
                r'(?:##\s*INTERVENTION\s+PRIORITY)[\s:]*\n*(.*?)$',
                r'(?:INTERVENTION\s+PRIORITY)[\s:]*\n*(.*?)$'
            ]
        }
        
        for section_name, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    sections[section_name] = match.group(1).strip()
                    break

        return sections
    
    def _format_overview_section(self, text: str) -> str:
        """Format the classroom overview section."""
        if not text:
            return "Classroom overview not available."
        
        text = self._clean_text(text)
        
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text

    def _format_performance_highlights(self, text: str) -> str:
        """Format the performance highlights section."""
        if not text:
            return "Performance highlights not available."
        
        text = self._clean_text(text)
        
        # Ensure student IDs are properly formatted
        text = re.sub(r'\bID-?(\w+)', r'ID-\1', text)
        
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text

    def _format_time_recommendations(self, text: str) -> str:
        """Format the time-based recommendations section."""
        if not text:
            return "Time-based recommendations not available."
        
        text = self._clean_text(text)
        
        # Ensure time periods are clearly formatted
        text = re.sub(r'(\d+)-(\d+)\s*min', r'\1-\2 minutes', text)
        
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text

    def _format_student_interventions(self, text: str) -> str:
        """Format the student interventions section."""
        if not text:
            return "Student intervention recommendations not available."
        
        text = self._clean_text(text)
        
        # Ensure student IDs are properly formatted
        text = re.sub(r'\bID-?(\w+)', r'ID-\1', text)
        
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text

    def _format_management_strategies(self, text: str) -> List[str]:
        """Format the classroom management strategies into a list."""
        if not text:
            return ["No management strategies provided."]
        
        strategies = []
        
        # Look for numbered strategies
        numbered_pattern = r'(\d+)\.\s*\*\*([^*]+)\*\*:?\s*(.*?)(?=(?:\d+\.|$))'
        matches = re.findall(numbered_pattern, text, re.DOTALL)
        
        if matches:
            for num, title, content in matches:
                strategy = f"{title.strip()}: {content.strip()}"
                if not strategy.endswith(('.', '!', '?')):
                    strategy += '.'
                strategies.append(strategy)
        else:
            # Fallback: split by common patterns
            lines = text.split('\n')
            current_strategy = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if re.match(r'^\d+\.', line) or re.match(r'^\*\*', line):
                    if current_strategy:
                        strategies.append(self._clean_strategy(current_strategy))
                    current_strategy = line
                else:
                    current_strategy += " " + line if current_strategy else line
            
            if current_strategy:
                strategies.append(self._clean_strategy(current_strategy))
        
        return strategies[:4]  # Limit to 4 strategies as requested

    def _clean_strategy(self, strategy: str) -> str:
        """Clean individual strategy text."""
        strategy = strategy.strip()
        
        # Remove numbers and asterisks
        strategy = re.sub(r'^\d+\.\s*', '', strategy)
        strategy = re.sub(r'\*\*([^*]+)\*\*:?\s*', r'\1: ', strategy)
        
        # Ensure proper capitalization
        if strategy:
            strategy = strategy[0].upper() + strategy[1:] if len(strategy) > 1 else strategy.upper()
        
        # Ensure proper punctuation
        if strategy and not strategy.endswith(('.', '!', '?')):
            strategy += '.'
        
        return strategy

    def _format_intervention_priority(self, text: str) -> Dict[str, any]:
        """Format the intervention priority section."""
        if not text:
            return {
                "high_priority": [],
                "medium_priority": [],
                "peak_times": [],
                "urgency_level": "Unknown"
            }
        
        text = self._clean_text(text)
        
        # Extract high priority students
        high_priority_match = re.search(r'high\s+priority[^:]*:?\s*([^-\n]*)', text, re.IGNORECASE)
        high_priority = self._extract_student_ids(high_priority_match.group(1) if high_priority_match else "")
        
        # Extract medium priority students
        medium_priority_match = re.search(r'medium\s+priority[^:]*:?\s*([^-\n]*)', text, re.IGNORECASE)
        medium_priority = self._extract_student_ids(medium_priority_match.group(1) if medium_priority_match else "")
        
        # Extract peak distraction times
        peak_times_match = re.search(r'peak\s+distraction\s+times?[^:]*:?\s*([^-\n]*)', text, re.IGNORECASE)
        peak_times = self._extract_time_periods(peak_times_match.group(1) if peak_times_match else "")
        
        # Extract urgency level
        urgency_match = re.search(r'\b(low|medium|high)\b.*urgency', text, re.IGNORECASE)
        urgency_level = urgency_match.group(1).title() if urgency_match else "Medium"
        
        return {
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "peak_times": peak_times,
            "urgency_level": urgency_level
        }

    def _extract_student_ids(self, text: str) -> List[str]:
        """Extract student IDs from text."""
        if not text:
            return []
        
        # Find all ID patterns
        id_matches = re.findall(r'ID-?(\w+)', text, re.IGNORECASE)
        return [f"ID-{id_match}" for id_match in id_matches]

    def _extract_time_periods(self, text: str) -> List[str]:
        """Extract time periods from text."""
        if not text:
            return []
        
        # Find time patterns like "5-7 minutes", "18-22", etc.
        time_matches = re.findall(r'(\d+)-(\d+)\s*(?:min|minutes?)?', text)
        return [f"{start}-{end} minutes" for start, end in time_matches]
    
    def _create_full_classroom_report(self, sections: Dict[str, str], class_name: str, class_id: str) -> str:
        """Create a nicely formatted full classroom report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
CLASSROOM FOCUS REPORT
{'='*60}
Class: {class_name} (ID: {class_id})
Generated: {timestamp}

CLASSROOM OVERVIEW
{'-'*40}
{self._format_overview_section(sections.get('overview', ''))}

PERFORMANCE HIGHLIGHTS
{'-'*40}
{self._format_performance_highlights(sections.get('performance', ''))}

TIME-BASED RECOMMENDATIONS
{'-'*40}
{self._format_time_recommendations(sections.get('time_recommendations', ''))}

STUDENT INTERVENTIONS
{'-'*40}
{self._format_student_interventions(sections.get('interventions', ''))}

CLASSROOM MANAGEMENT STRATEGIES
{'-'*40}
"""
        
        strategies = self._format_management_strategies(sections.get('strategies', ''))
        for i, strategy in enumerate(strategies, 1):
            report += f"{i}. {strategy}\n"
        
        priority = self._format_intervention_priority(sections.get('priority', ''))
        
        report += f"""

INTERVENTION PRIORITY
{'-'*40}
High Priority Students: {', '.join(priority['high_priority']) if priority['high_priority'] else 'None'}
Medium Priority Students: {', '.join(priority['medium_priority']) if priority['medium_priority'] else 'None'}
Peak Distraction Times: {', '.join(priority['peak_times']) if priority['peak_times'] else 'None identified'}
Overall Urgency Level: {priority['urgency_level']}
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

