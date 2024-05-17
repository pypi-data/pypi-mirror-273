import unittest
from unittest.mock import MagicMock
import requests
from ..src.ai_models.text_extract import pdf_extract, web_extract, image_text_detection, speech_to_text

class TestFunctions(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_pdf_extract(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test pdf extraction result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = pdf_extract(api_key=self.api_key, pdf_file=MagicMock(name="mock_pdf_file"))

        self.assertEqual(result, '{"result": "Test pdf extraction result"}')
        requests_mock.request.assert_called_once()

    def test_web_extract(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test web extraction result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = web_extract(api_key=self.api_key, url_search="www.example.com")

        self.assertEqual(result, '{"result": "Test web extraction result"}')
        requests_mock.request.assert_called_once()

    def test_image_text_detection(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test image text detection result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = image_text_detection(api_key=self.api_key, image_file=MagicMock(name="mock_image_file"))

        self.assertEqual(result, '{"result": "Test image text detection result"}')
        requests_mock.request.assert_called_once()

    def test_speech_to_text(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test speech to text result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = speech_to_text(api_key=self.api_key, audio_file=MagicMock(name="mock_audio_file"))

        self.assertEqual(result, '{"result": "Test speech to text result"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
