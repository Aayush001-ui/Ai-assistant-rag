import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

class OllamaClient:
    def __init__(self):
        self.url = f"{OLLAMA_BASE_URL}/api/generate"

    def generate_response(self, prompt: str) -> str:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"