import os
import requests

def search_ai_v2(question="", training_data="", api_key=None):
    if question == "":
        return "Question is incomplete. Please give a question and try again."
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/search/v2"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "question": question,
        "training_data": training_data
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.text

def search_ai_v3(question="", training_data="", search_count=10, api_key=None):
    if question == "":
        return "Question is incomplete. Please give a question and try again"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/search/v3"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "question": question,
        "training_data": training_data,
        "search_count": search_count
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.text
