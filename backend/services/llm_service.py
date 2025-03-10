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
            
            # Extract mark from the response
            try:
                # Find and extract the mark
                for line in feedback_text.split("\n"):
                    if line.startswith("MARK:"):
                        mark_text = line.replace("MARK:", "").strip()
                        # Extract the first number if there's a format like "8/10"
                        if "/" in mark_text:
                            mark_text = mark_text.split("/")[0]
                        marks = float(mark_text)
                        break
                else:
                    # If no mark found, log warning and default to 0
                    logger.warning("No mark found in LLM response")
                    marks = 0.0
                
                # The rest of the text is the feedback
                feedback_markdown = feedback_text
                
                logger.info(f"Successfully generated feedback with mark: {marks}")
                return feedback_markdown, marks
                
            except Exception as e:
                logger.error(f"Error extracting mark from response: {str(e)}")
                # Return the whole response and a default mark
                return feedback_text, 0.0

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            raise

    def _create_prompt(self, criteria_markdown, homework_markdown):
        """Create the prompt for the LLM"""
        return f"""
# Imagine that you are a Year 12 HSC Business Studies teacher in NSW, Australia. 
# Task: Grade the following student homework based on the provided marking criteria.
# All documents are in markdown format, keep your response in markdown format.

## Marking Criteria:
{criteria_markdown}

## Student Submission:
{homework_markdown}

Based on the marking criteria and the student's submission, provide:

1. Detailed, constructive feedback on the submission. Use dot point format. One dot point to summarise strengths and a few dot points for areas for improvement. 
2. A numerical mark according to the marking criteria. The total mark is given in the marking criteria. Be strict with the marking criteria, full marks should only be given for perfect submissions.

Format your response as follows:

MARK: [numerical mark/total mark]

FEEDBACK:
[Your detailed feedback here]
"""
