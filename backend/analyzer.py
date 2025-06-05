import os
import requests

OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def extract_text(data: bytes) -> str:
    """Decode bytes to text, ignoring errors."""
    return data.decode("utf-8", errors="ignore")


def analyze_text(prompt: str, text: str) -> str:
    """Send the prompt and text to OpenRouter and return the result."""
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful document analyzer."},
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ]
    }
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    return result.get("choices", [{}])[0].get("message", {}).get("content", "")
