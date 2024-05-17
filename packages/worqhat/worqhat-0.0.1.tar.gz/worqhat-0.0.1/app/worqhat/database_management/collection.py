import requests
import os 

def create_collection(collection='', collection_schema='', collection_sort_by='',api_key=None ):
    if collection=='':
        return ("Please enter a Collection name")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/collections/create"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "collection": collection,
        "collectionSchema": collection_schema,
        "collectionSortBy": collection_sort_by
    }

    response = requests.post("POST",url, json=payload, headers=headers)

    return response.text