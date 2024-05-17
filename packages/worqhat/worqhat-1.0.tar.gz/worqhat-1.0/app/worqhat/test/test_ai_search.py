import unittest
from unittest.mock import MagicMock
from ..src.ai_models.ai_search import search_ai_v2, search_ai_v3

class TestAISearch(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_search_ai_v2(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test result for AI v2"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('ai_search.requests', requests_mock):
            result = search_ai_v2(api_key=self.api_key, question="Test question")

        self.assertEqual(result, '{"result": "Test result for AI v2"}')
        requests_mock.request.assert_called_once()

    def test_search_ai_v3(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test result for AI v3"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('ai_search.requests', requests_mock):
            result = search_ai_v3(api_key=self.api_key, question="Test question")

        self.assertEqual(result, '{"result": "Test result for AI v3"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
