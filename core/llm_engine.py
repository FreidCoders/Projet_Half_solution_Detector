import requests

class OllamaClient:
    def __init__(self, base_url: str, model: str, timeout: int = 180):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def check_connection(self):
        response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()
        models = [m.get("name", "") for m in response.json().get("models", [])]
        if not any(name == self.model or name.startswith(self.model + ":") for name in models):
            raise RuntimeError(
                f"Modèle '{self.model}' introuvable. Modèles installés : {', '.join(models) or 'aucun'}"
            )

    def generate_json(self, prompt: str):
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.1},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        import json
        return json.loads(payload["response"])
