import unittest
from unittest.mock import MagicMock
import requests
from ..src.ai_models.image_analysis import image_analysis, face_detection, facial_comparison

class TestImageFunctions(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_image_analysis(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test image analysis result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = image_analysis(api_key=self.api_key, images=[MagicMock(name="mock_image")], question="Test question")

        self.assertEqual(result, '{"result": "Test image analysis result"}')
        requests_mock.request.assert_called_once()

    def test_face_detection(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test face detection result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = face_detection(api_key=self.api_key, image_file=MagicMock(name="mock_image_file"))

        self.assertEqual(result, '{"result": "Test face detection result"}')
        requests_mock.request.assert_called_once()

    def test_facial_comparison(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"result": "Test facial comparison result"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = facial_comparison(api_key=self.api_key, source_image_file=MagicMock(name="mock_source_image_file"), target_image_file=MagicMock(name="mock_target_image_file"))

        self.assertEqual(result, '{"result": "Test facial comparison result"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
