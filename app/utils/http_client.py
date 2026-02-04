import requests

def post(url, headers, payload):
    return requests.post(url, headers=headers, json=payload)

