import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../..')))

from backend.services.llm_service import LLMService


class TestLLMService(unittest.TestCase):
    """
    Test cases for the LLMService class.
    """

    @patch('backend.services.llm_service.OPENAI_API_KEY', 'test_api_key')
    @patch('backend.services.llm_service.LLM_MODEL', 'test-model')
    @patch('backend.services.llm_service.LLM_TEMPERATURE', 1)
    @patch('backend.services.llm_service.LLM_MAX_TOKENS', 1000)
    def test_init(self):
        """Test LLMService initialization."""
        service = LLMService()
        
        self.assertEqual(service.api_key, 'test_api_key')
        self.assertEqual(service.model, 'test-model')
        self.assertEqual(service.temperature, 1)
        self.assertEqual(service.max_tokens, 1000)

    def test_create_prompt(self):
        """Test prompt creation."""
        service = LLMService()
        criteria = "# Criteria\n- Point 1\n- Point 2"
        homework = "# Homework\nStudent's work here."
        
        prompt = service._create_prompt(criteria, homework)
        
        self.assertIn("## Marking Criteria:", prompt)
        self.assertIn(criteria, prompt)
        self.assertIn("## Student Submission:", prompt)
        self.assertIn(homework, prompt)
        self.assertIn("MARK: [numerical mark/total mark]", prompt)

    @patch('requests.post')
    def test_generate_feedback_success(self, mock_post):
        """Test successful feedback generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "MARK: 7.5/10\n\nFEEDBACK:\n- Strong analysis\n- Needs better structure"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Create service and generate feedback
        service = LLMService()
        feedback, marks = service.generate_feedback(
            "Test criteria", "Test homework"
        )
        
        # Verify results
        self.assertEqual(marks, 7.5)
        self.assertEqual(feedback, "MARK: 7.5/10\n\nFEEDBACK:\n- Strong analysis\n- Needs better structure")
        
        # Verify API call
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://api.openai.com/v1/chat/completions")
        
        # Verify payload
        payload = json.loads(call_args[1]['data'])
        self.assertEqual(payload['model'], service.model)
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(payload['temperature'], service.temperature)

    @patch('requests.post')
    def test_generate_feedback_with_fraction_mark(self, mock_post):
        """Test feedback generation with a mark in fraction format."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "MARK: 8/10\n\nFEEDBACK:\n- Good work\n- Need improvement"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Create service and generate feedback
        service = LLMService()
        feedback, marks = service.generate_feedback(
            "Test criteria", "Test homework"
        )
        
        # Verify mark extraction with fraction
        self.assertEqual(marks, 8.0)
        self.assertEqual(feedback, "MARK: 8/10\n\nFEEDBACK:\n- Good work\n- Need improvement")

    @patch('requests.post')
    def test_generate_feedback_no_mark(self, mock_post):
        """Test feedback generation without a mark."""
        # Setup mock response with no mark
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "FEEDBACK:\n- Missing mark\n- But still has feedback"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        # Create service and generate feedback
        service = LLMService()
        feedback, marks = service.generate_feedback(
            "Test criteria", "Test homework"
        )
        
        # Verify results (should default to 0.0 mark)
        self.assertEqual(marks, 0.0)
        self.assertEqual(feedback, "FEEDBACK:\n- Missing mark\n- But still has feedback")

    @patch('requests.post')
    def test_generate_feedback_api_error(self, mock_post):
        """Test API error handling."""
        # Setup mock to raise an exception
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_post.return_value = mock_response
        
        # Create service and attempt to generate feedback
        service = LLMService()
        with self.assertRaises(Exception):
            service.generate_feedback("Test criteria", "Test homework")


if __name__ == "__main__":
    unittest.main() 