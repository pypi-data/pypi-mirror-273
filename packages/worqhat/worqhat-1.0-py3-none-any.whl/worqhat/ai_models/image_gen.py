import requests
import os


def generate_image_v2(prompt=[""], image_style="realistic", output_type="url", orientation="square", api_key=None):
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
         raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/generate/v2"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "image_style": image_style,
        "output_type": output_type,
        "orientation": orientation
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def generate_image_v3(prompt=[], image_style="realistic", output_type="url", orientation="square", api_key=None):
    if not api_key:
        api_key = os.getenv("API_KEY")

    if not api_key:
         raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/generate/v3"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "image_style": image_style,
        "output_type": output_type,
        "orientation": orientation
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text

def modify_image_v2(image=None,modification=None, output_type="URL", similarity="30",  api_key=None):
    if not modification:
        return "Modification description is missing"
    if not image or len(image) == 0:
        return "Image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
         raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/modify/v2"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
            "modification": modification,
            "output_type": output_type,
            "similarity": similarity
        }
    if image.startswith('http://') or image.startswith('https://'):
        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'application/octet-stream'))]
    else:
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'application/octet-stream'))]
    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text


def modify_image_v3(image=None,modification=None, output_type="URL", similarity="30",  api_key=None):
    if not modification:
        return "Modification description is missing"
    if not image or len(image) == 0:
        return "Existing images are missing"
    if not api_key:
        api_key = os.getenv("API_KEY")

    # If api_key is still not available, return an error message
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    url = "https://api.worqhat.com/api/ai/images/modify/v3"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }



        # Prepare payload
    payload = {
            "modification": modification,
            "output_type": output_type,
            "similarity": similarity
        }

        # Prepare files data in the required format
    if image.startswith('http://') or image.startswith('https://'):
            # If image is a URL, download the image content
        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'application/octet-stream'))]
    else:
        # If image is a local file path, read the file content
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'application/octet-stream'))]

        # Make the API call
    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

def remove_text_from_image(image=None,output_type="URL",  api_key=None):

    if not image:
        return "Existing image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/modify/v3/remove-text"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {'output_type': output_type}

    if image.startswith('http://') or image.startswith('https://'):
        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]

    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

def remove_background_from_image(existing_image=None,output_type="URL",  api_key=None):
    if not existing_image:
        return "Existing image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
       raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    url = "https://api.worqhat.com/api/ai/images/modify/v3/remove-background"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {'output_type': output_type}
    if existing_image.startswith('http://') or existing_image.startswith('https://'):
        response = requests.get(existing_image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
        with open(existing_image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]
    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

def replace_background(image=None,modification=None, output_type="URL",  api_key=None):
    if not modification:
        return "Modification description is missing"
    if not image:
        return "Existing image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    url = "https://api.worqhat.com/api/ai/images/modify/v3/replace-background"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "modification": modification,
        "output_type": output_type
    }

    if image.startswith('http://') or image.startswith('https://'):
        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]
    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

def search_replace_image(image=None,modification=None, output_type="URL", search_object=None,  api_key=None):
    if not modification:
        return "Modification description is missing"
    if not search_object:
        return "Search object description is missing"
    if not image:
        return "Existing image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    url = "https://api.worqhat.com/api/ai/images/modify/v3/search-replace-image"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "modification": modification,
        "output_type": output_type,
        "search_object": search_object
    }

    if image.startswith('http://') or image.startswith('https://'):

        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
  
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]
    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text


def extend_image(image=None,output_type="URL", left_extend="100", right_extend="100", top_extend="50", bottom_extend="50", description="",  api_key=None):
    if not image:
        return "image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    url = "https://api.worqhat.com/api/ai/images/modify/v3/extend-image"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "output_type": output_type,
        "leftExtend": left_extend,
        "rightExtend": right_extend,
        "topExtend": top_extend,
        "bottomExtend": bottom_extend,
        "description": description
    }

    if image.startswith('http://') or image.startswith('https://'):

        response = requests.get(image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
        with open(image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]

    response = requests.post(url, headers=headers, data=payload, files=files)
    return response.text

def upscale_image(existing_image=None,scale="4", output_type="URL",api_key=None):
    if not existing_image:
        return "Existing image is missing"
    if not api_key:
        api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    url = "https://api.worqhat.com/api/ai/images/upscale/v3"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "scale": scale,
        "output_type": output_type
    }

    if existing_image.startswith('http://') or existing_image.startswith('https://'):

        response = requests.get(existing_image)
        files = [('existing_image', ('file', response.content, 'image/png'))]
    else:
        with open(existing_image, 'rb') as f:
            files = [('existing_image', ('file', f, 'image/png'))]

    response = requests.post(url, headers=headers, data=payload, files=files)

    return response.text