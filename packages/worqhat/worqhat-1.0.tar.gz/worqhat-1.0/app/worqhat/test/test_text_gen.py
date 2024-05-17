import unittest
from unittest.mock import MagicMock
import requests
from ..src.ai_models.text_gen import (get_ai_responsev2, get_ai_responsev3, 
                         get_large_ai_response_v2, get_alpha_ai_response)

class TestAIResponses(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_get_ai_responsev2(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"response": "Test AI response v2"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = get_ai_responsev2(api_key=self.api_key, question="What is the capital of India?")

        self.assertEqual(result, '{"response": "Test AI response v2"}')
        requests_mock.request.assert_called_once()

    def test_get_ai_responsev3(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"response": "Test AI response v3"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = get_ai_responsev3(api_key=self.api_key, question="What is the capital of India?")

        self.assertEqual(result, '{"response": "Test AI response v3"}')
        requests_mock.request.assert_called_once()

    def test_get_large_ai_response_v2(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"response": "Test Large AI response v2"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = get_large_ai_response_v2(api_key=self.api_key, question="What is the capital of Delhi?", dataset_id="123456789")

        self.assertEqual(result, '{"response": "Test Large AI response v2"}')
        requests_mock.request.assert_called_once()

    def test_get_alpha_ai_response(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"response": "Test Alpha AI response"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = get_alpha_ai_response(api_key=self.api_key, question="What is the capital of Delhi?")

        self.assertEqual(result, '{"response": "Test Alpha AI response"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
