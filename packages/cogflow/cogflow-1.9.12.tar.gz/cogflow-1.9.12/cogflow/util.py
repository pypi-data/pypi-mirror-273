"""
    Utility functions
"""

import requests


def make_post_request(url, data=None, params=None):
    """
        utility function to make POST requests
    :param url: url of the API endpoint
    :param data: JSON payload
    :param params: request params
    :return: response for the POST request in json format
    """
    try:
        if data:
            response = requests.post(url, json=data, params=params)
        else:
            response = requests.post(url, params=params)

        if response.status_code == 201:
            print("POST request successful")
            return response.json()
        # if not the success response
        print(f"POST request failed with status code {response.status_code}")
        raise Exception("request failed")
    except requests.exceptions.RequestException as e:
        print(f"Error making POST request: {e}")
        raise Exception(f"Error making POST request: {e}")
