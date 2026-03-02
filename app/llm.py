import requests
from app.config import HUGGINGFACE_TOKEN

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}

def generate_response(prompt: str) -> str:
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        print("HF STATUS:", response.status_code)
        print("HF RESPONSE:", response.text)

        if response.status_code != 200:
            return f"HF Error: {response.text}"

        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "")

        return str(result)

    except Exception as e:
        return f"Exception: {str(e)}"