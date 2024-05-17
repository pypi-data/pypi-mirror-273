import requests
import os
import json

def analyze_images(images, question="", training_data="", output_type="text", stream_data=False, api_key=None):
    if not images or len(images) == 0:
        return "No images found. Please try again "

    api_key = api_key or os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/v2/image-analysis"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'output_type': output_type,
        'stream_data': str(stream_data).lower(),
        'question': question,
        'training' : training_data
    }
    files = []
    for image in images:
        if image.startswith('http://') or image.startswith('https://'):
            response = requests.get(image)
            files.append(('images', (os.path.basename(image), response.content, 'image/jpeg')))
        else:
            with open(image, 'rb') as f:
                file_content = f.read()
                files.append(('images', (os.path.basename(image), file_content, 'image/jpeg')))
    response = requests.post(url, headers=headers, data=payload, files=files)
    if stream_data:
        for line in response.iter_lines():
            if line:
                if line.startswith(b'data:'):
                    json_content = line[len(b'data:'):].decode('utf-8').strip()
                    print(json_content)
    else:
        json_response = response.text
        try:
            json_data = json.loads(json_response)
            print(json.dumps(json_data, indent=4))
        except json.JSONDecodeError:
            print(json_response)

def detect_faces(image, api_key=None):
    if not image or len(image) == 0:
        return "No images found. Please try again "
    api_key = api_key or os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/v2/face-detection"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    if image.startswith('http://') or image.startswith('https://'):
        response = requests.get(image)
        file=[('image', (os.path.basename(image), response.content, 'image/jpeg'))]
    else:
        with open(image, 'rb') as f:
            file=[('image', (os.path.basename(image), f, 'image/jpeg'))]
    response = requests.post(url, headers=headers, files=file)
    return response.text

def compare_faces(source_image, target_image, api_key=None):
    if not source_image or not target_image:
        return "No images found. Please try again "
    api_key = api_key or os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/v2/facial-comparison"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
   
    if source_image.startswith('http://') or source_image.startswith('https://'):
        response = requests.get(source_image)
        source_file=[('source_image', (os.path.basename(source_image), response.content, 'image/jpeg'))]
    else:
        with open(source_image, 'rb') as f:
           source_file=[('source_image', (os.path.basename(source_image), f, 'image/jpeg'))]
    if target_image.startswith('http://') or target_image.startswith('https://'):
        response = requests.get(target_image)
        target_file=[('target_image', (os.path.basename(target_image), response.content, 'image/jpeg'))]
    else:
        with open(target_image, 'rb') as f:
            target_file=[('target_image', (os.path.basename(target_image), f, 'image/jpeg'))]
    files = source_file + target_file
    response = requests.post(url, headers=headers, files=files)
    return response.text
