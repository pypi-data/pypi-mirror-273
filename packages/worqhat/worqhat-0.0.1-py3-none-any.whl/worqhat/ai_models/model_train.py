import requests 
import os


def list_datasets(api_key=None):
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/list-datasets"
    headers = {"Authorization": "Bearer " + api_key}
    response = requests.post(url, headers=headers)
    return response.text
    
def delete_dataset(dataset_id="", api_key=None):
    if dataset_id=="":
        raise ValueError("No Dataset Id provided")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = f"https://api.worqhat.com/api/delete-datasets/{dataset_id}"
    headers = {"Authorization": "Bearer " + api_key}
    response = requests.post(url, headers=headers)
    return response.text

    
def train_dataset(dataset_id="", dataset_name="", dataset_type="", json_data="", training_file=None, api_key=None):
    if dataset_id=="":
        raise ValueError("No Dataset Id provided")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/datasets/train-datasets"
    headers = {"Authorization": "Bearer " + api_key}
    payload = {
            "datasetId": dataset_id,
            "dataset_name": dataset_name,
            "dataset_type": dataset_type,
            "json_data": (None, json_data),
            "training_file": (training_file, open(training_file, 'rb'))
    }
    response = requests.post(url, files=payload, headers=headers)
    return response.text
