import requests
import os 


def add_data_to_collection(collection='', doc_id='', data='',api_key=None ):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/add"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "collection": collection,
        "docId": doc_id,
        "data": data
    }

    response = requests.post("POST",url, json=payload, headers=headers)

    return response.text

def update_data_in_collection( collection='', doc_id='', data='',api_key=None):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/update"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "collection": collection,
        "docId": doc_id,
        "data": data
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text

def increment_field_in_collection(collection='', doc_id='', field='', increment_value='',api_key=None):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/increment"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "collection": collection,
        "docId": doc_id,
        "field": field,
        "increment": increment_value
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text

def update_array_in_collection(collection='', doc_id='', field='', value='',api_key=None ):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/array/update/add"
    payload = {
        "collection": collection,
        "docId": doc_id,
        "field": field,
        "arrayUnion": value
    }
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text

def remove_array_element_from_collection(collection='', doc_id='', field='', value='',api_key=None):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/array/update/remove"
    payload = {
        "collection": collection,
        "docId": doc_id,
        "field": field,
        "arrayRemove": value
    }
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text

def delete_doc_from_collection(collection='', doc_id='',api_key=None):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/data/delete"
    payload = {
        "collection": collection,
        "docId": doc_id
    }
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.text
