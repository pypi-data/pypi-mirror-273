import requests 
import json
import os
def get_ai_response_v2(question="", 
                       preserve_history=False, 
                       randomness=0.5, 
                       stream_data=False, 
                       conversation_history=[], 
                       training_data="", 
                       response_type="text",
                       api_key=None):
    url = "https://api.worqhat.com/api/ai/content/v2"

    payload = {
        "question": question,
        "preserve_history": preserve_history,
        "randomness": randomness,
        "stream_data": stream_data,
        "conversation_history": conversation_history,
        "training_data": training_data,
        "response_type": response_type
    }

    headers = {"Content-Type": "application/json"}

    if not api_key:
        api_key = os.getenv("API_KEY")

    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    else:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    response = requests.post(url, json=payload, headers=headers, stream=stream_data)

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
            return(json.dumps(json_data, indent=4))
        except json.JSONDecodeError:
            print(json_response)


def get_ai_response_v3(question="", 
                       preserve_history=False, 
                       randomness=0.5, 
                       stream_data=False, 
                       conversation_history=[], 
                       training_data="", 
                       response_type="text",
                       api_key=None):
    url = "https://api.worqhat.com/api/ai/content/v3"

    payload = {
        "question": question,
        "preserve_history": preserve_history,
        "randomness": randomness,
        "stream_data": stream_data,
        "conversation_history": conversation_history,
        "training_data": training_data,
        "response_type": response_type
    }

    headers = {"Content-Type": "application/json"}

    if not api_key:
        api_key = os.getenv("API_KEY")

    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    else:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")

    response = requests.post(url, json=payload, headers=headers, stream=stream_data)

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


def get_alpha_ai_response(question="", 
                          preserve_history=False, 
                          randomness=0.5, 
                          stream_data=False, 
                          conversation_history=[], 
                          training_data="", 
                          response_type="text",
                          api_key=None):
    url = "https://api.worqhat.com/api/ai/content/v3/alpha"
    payload = {
        "question": question,
        "preserve_history": preserve_history,
        "randomness": randomness,
        "stream_data": stream_data,
        "conversation_history": conversation_history,
        "training_data": training_data,
        "response_type": response_type
    }
    headers = {"Content-Type": "application/json"}
    if not api_key:
        api_key = os.getenv("API_KEY")
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    else:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    response = requests.request("POST",url, json=payload, headers=headers)
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


def get_large_ai_response_v2(question="", 
                             dataset_id="", 
                             preserve_history=True, 
                             randomness=0.5, 
                             stream_data=False, 
                             conversation_history=[], 
                             instructions=None,
                             api_key=None):
    url = "https://api.worqhat.com/api/ai/content/v2-large/answering"
    payload = {
        "question": question,
        "datasetId": dataset_id,
        "preserve_history": preserve_history,
        "randomness": randomness,
        "stream_data": stream_data,
        "conversation_history": conversation_history,
        "instructions": instructions
    }
    headers = {"Content-Type": "application/json"}
    if not api_key:
        api_key = os.getenv("API_KEY")
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    else:
        raise ValueError("API key is missing. Provide it as an argument or in the .env file.")
    response = requests.request("POST",url, json=payload, headers=headers)
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
