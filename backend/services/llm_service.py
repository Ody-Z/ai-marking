import logging
import requests
import json
from typing import Tuple
from backend.config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

logger = logging.getLogger(__name__)


class LLMService:
    """
    Handles interactions with the LLM API for generating feedback.
    """

    def __init__(self):
        logger.info(f"Initializing LLM Service using model: {LLM_MODEL}")
        self.api_key = OPENAI_API_KEY
        self.model = LLM_MODEL
        self.temperature = LLM_TEMPERATURE
        self.max_tokens = LLM_MAX_TOKENS

        if not self.api_key:
            logger.warning("No API key provided for the LLM service")

    def generate_feedback(self, criteria_markdown, homework_markdown):
        """
        Generate feedback and marks based on marking criteria and homework submission.

        Args:
            criteria_markdown (str): Markdown content of the marking criteria
            homework_markdown (str): Markdown content of the student's homework

        Returns:
            tuple: (feedback_markdown, marks)
        """
        logger.info("Generating feedback using LLM")

        # Prepare the prompt for the LLM
        prompt = self._create_prompt(criteria_markdown, homework_markdown)

        try:
            # Call the OpenAI API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are an AI assistant that generates feedback for student homework based on marking criteria."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )

            response.raise_for_status()
            response_data = response.json()

            # Extract the response content
            feedback_text = response_data["choices"][0]["message"]["content"]

            # Process the response to extract marks and feedback
            marks, feedback_markdown = self._process_response(feedback_text)

            logger.info(f"Successfully generated feedback with mark: {marks}")
            return feedback_markdown, marks

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            raise

    def _create_prompt(self, criteria_markdown, homework_markdown):
        """Create the prompt for the LLM"""
        return f"""
# Imagine that you are a Year 12 HSC Business Studies teacher in NSW, Australia. Task: Grade the following student homework based on the provided marking criteria.

## Marking Criteria:
{criteria_markdown}

## Student Submission:
{homework_markdown}

Based on the marking criteria and the student's submission, provide:

1. Detailed feedback on the submission, highlighting strengths and areas for improvement
2. A numerical mark according to the marking criteria
3. Specific recommendations for how the student can improve their work

Format your response as follows:

MARK: [numerical mark]

FEEDBACK:
[Your detailed feedback here]

RECOMMENDATIONS:
[Your specific recommendations for improvement]
"""

    def _process_response(self, response_text):
        """
        Process the LLM response to extract marks and feedback.

        Args:
            response_text (str): Raw response from the LLM

        Returns:
            tuple: (marks, feedback_markdown)
        """
        try:
            # Split the response into sections
            sections = response_text.split("\n\n")

            # Extract mark
            mark_line = next(line for line in sections[0].split(
                "\n") if line.startswith("MARK:"))
            marks = float(mark_line.replace("MARK:", "").strip())

            # Combine feedback and recommendations into markdown
            feedback_markdown = response_text.replace(mark_line, "").strip()

            return marks, feedback_markdown

        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
