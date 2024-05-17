import unittest
from unittest.mock import MagicMock
import requests
from ..src.ai_models.model_train import list_datasets, delete_dataset, train_dataset

class TestDatasetFunctions(unittest.TestCase):

    def setUp(self):
        # Mock API key for testing
        self.api_key = "mock_api_key"

    def test_list_datasets(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"datasets": ["Dataset1", "Dataset2"]}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = list_datasets(api_key=self.api_key)

        self.assertEqual(result, '{"datasets": ["Dataset1", "Dataset2"]}')
        requests_mock.request.assert_called_once()

    def test_delete_dataset(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"message": "Dataset deleted successfully"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = delete_dataset(api_key=self.api_key, dataset_id="123456789")

        self.assertEqual(result, '{"message": "Dataset deleted successfully"}')
        requests_mock.request.assert_called_once()

    def test_train_dataset(self):
        # Mock response
        mock_response = MagicMock()
        mock_response.text = '{"message": "Dataset trained successfully"}'
        requests_mock = MagicMock()
        requests_mock.request.return_value = mock_response

        with unittest.mock.patch('your_module.requests', requests_mock):
            result = train_dataset(api_key=self.api_key, dataset_id="123456789", dataset_name="Sample Dataset", dataset_type="self", json_data="{'data':'This is sample Data'}", training_file="sample_training_data.txt")

        self.assertEqual(result, '{"message": "Dataset trained successfully"}')
        requests_mock.request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
