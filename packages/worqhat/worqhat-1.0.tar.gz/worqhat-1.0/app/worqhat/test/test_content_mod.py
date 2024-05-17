import unittest
from unittest.mock import MagicMock
import requests
from ..src.ai_models.content_mod import content_moderation,image_moderation

class TestModeration(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_content_moderation(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test content moderation result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('moderation.requests', requests_mock):
            result = content_moderation(api_key=self.api_key, text_content="Test text content")

        self.assertEqual(result, '{"result": "Test content moderation result"}')
        requests_mock.request.assert_called_once()

    def test_image_moderation(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test image moderation result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('moderation.requests', requests_mock):
            result = image_moderation(api_key=self.api_key, image_file=MagicMock(name="mock_image_file"))

        self.assertEqual(result, '{"result": "Test image moderation result"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
