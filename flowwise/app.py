import requests

API_URL = "http://localhost:3000/api/v1/prediction/eeea81ea-1c4f-4bff-a36e-0b19bccc7881"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
    
output = query({
    "question": "Hey, how are you?",
})