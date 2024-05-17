import requests 
import os


def content_moderation(text_content="",api_key=None):
    if text_content == "":
        return "Text content is incomplete. Please give some text and try again. "
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/moderation"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text_content": text_content
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def image_moderation(image=None, api_key=None):
    if not image or len(image) == 0:
        return "No images found. Please try again "
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/v2/image-moderation"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
       
    if image.startswith('http://') or image.startswith('https://'):        
        response = requests.get(image)
        files = [('image', ('file', response.content, 'application/octet-stream'))]
    else:
        with open(image, 'rb') as f:
            files = [('image', ('file', f, 'application/octet-stream'))]
    response = requests.post(url, files=files, headers=headers)
    return response.text

    