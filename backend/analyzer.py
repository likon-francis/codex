import os

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
