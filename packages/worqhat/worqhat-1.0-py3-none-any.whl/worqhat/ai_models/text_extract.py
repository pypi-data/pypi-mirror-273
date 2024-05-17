import requests
import os


def extract_pdf_text(pdf_file=None, api_key=None):
    if not pdf_file:
        return "PDF file is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
        print(api_key)
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/v2/pdf-extract"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = [('file', (os.path.basename(pdf_file), open(pdf_file, 'rb'), 'application/pdf'))]
    response = requests.post(url, files=files, headers=headers)
    return response.text

def web_extract(url_search="", headline=True, inline_code=True, code_blocks=True, references=True, tables=True, api_key=None):
    if url_search=="":
        raise ValueError("No URL provided")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/v2/web-extract"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "url_path": url_search,
        "headline": headline,
        "inline_code": inline_code,
        "code_blocks": code_blocks,
        "references": references,
        "tables": tables
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text


def detect_image_text(image=None, output_type="text", api_key=None):

    if not image or len(image) == 0:
        raise ValueError("Images are missing")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/v2/image-text-detection"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    results = []
    payload = {'output_type': output_type}
    if image.startswith('http://') or image.startswith('https://'):
        response = requests.get(image)
        files = [('image', (os.path.basename(image), response.content, 'image/jpeg'))]
    else:
        with open(image, 'rb') as f:
            files = [('image', (os.path.basename(image), f, 'image/jpeg'))]
        response = requests.post(url, headers=headers, data=payload, files=files)
        results.append(response.text)
    return results


def convert_speech_to_text(audio_file=None, api_key=None):
    if not audio_file:
        raise ValueError("Audio file is missing")
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/speech-text"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = [('audio', (os.path.basename(audio_file), open(audio_file, 'rb'), 'application/octet-stream'))]
    response = requests.post(url, files=files, headers=headers)
    return response.text