import google.generativeai as genai
import os 
import sys
import logging

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

class GeminiReportGenerator:
    """
    Gemini model for generating student focus reports.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the gemini model using config

        Args:
            model_name (str): The name of the Gemini model to use.
        """
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)

        # configure Gemini with Api key from config
        genai.configure(api_key=Config.Gemini_API_KEY)
        self.model = genai.GenerativeModel(self.model_name)

    def generate_report(self, prompt: str, temperature: float = 0.7) -> dict:
        """
        Generate a report using gemini model.

        Args:
            prompt(str): The formatted prompt from report_prompt.py.
            temperature(float): controls randomness (0.0 to 1.0)

            Returns:
                dict: contains success status and report text.
        """
        try:
            # Configure generation
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1000,
            )

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )

            if response.text:
                return {
                    "success": True,
                    "report": response.txt.strip()
                }
            else:
                return {
                    "success": False,
                    "error": "No content generated"
                }
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    def test_connection(self) -> bool:
        """
        Test if the Gemini model is reachable.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.model.generate_content("Test connection")
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
        
