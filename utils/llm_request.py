import requests
from time import time
from .llm_parameters import Params


def send_prompt(prompt: str, params: Params):
    """
    Sends prompt to perplexity.ai
    prompt: str = string of prompt to ask the model
    params.model: str = name of the model
    params.token: str = token to access the api

    Returns dictionary:
        model = name of used model
        content = content of the response
        duration = time model needed for answer
        status = request status or -1 in case of timeout
    """

    payload = {
        'model': params.model,
        'messages': [
            {'role': 'system', 'content': 'You are expert on DnD 5e (2024).'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.5,
    }

    try:
        start_time = time()
        result: requests.Response = requests.post(
            params.url,
            headers={'Authorization': f'Bearer {params.token}'},
            json=payload,
            stream=False,
        )
        end_time = time()

    except requests.exceptions.ReadTimeout:
        result_dict = {
            'model': params.model,
            'content': '',
            'duration': end_time - start_time,
            'status': -1
        }
        return result_dict

    if result.status_code != 200:
        result_dict = {
            'model': params.model,
            'content': result.content,
            'duration': end_time - start_time,
            'status': result.status_code
        }
        return result_dict
    result_json = result.json()['choices'][0]
    if 'message' in result_json:
        message = result_json['message']['content']
        result_dict = {
            'model': params.model,
            'content': message,
            'duration': end_time - start_time,
            'status': result.status_code
        }
    return result_dict
