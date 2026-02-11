import requests


def chat_with_ollama(prompt, model="tiny_model:latest"):
    """Ask Ollama a question and get a response."""
    
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
        }
    }
    
    try:
        print(f" Sending to {model}...")
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "No response")
    except Exception as e:
        return f" Error: {str(e)}"


if __name__ == "__main__":
    # Simple example
    answer = chat_with_ollama("What did you mean by molecular Dynamics")
    print(answer)
