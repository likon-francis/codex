import os
from io import BytesIO
import requests
from PyPDF2 import PdfReader
from docx import Document as DocxDocument

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    "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",
)
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# Default system prompts for different analysis scenarios. The user provided
# `analysis_type` selects one of these prompts. It can be extended as needed
# for new scenarios.
ANALYSIS_PRESETS = {
    "cv": (
        "You are a recruitment assistant. Analyse the CV and provide a concise "
        "summary of key skills and experience."
    ),
    "tender": (
        "You are a tender evaluation assistant. Highlight compliance issues and "
        "summarise requirements."
    ),
}


def list_presets() -> list[dict]:
    """Return available analysis types and their system prompts."""
    return [
        {"type": k, "prompt": v} for k, v in ANALYSIS_PRESETS.items()
    ]


def extract_text(data: bytes, filename: str) -> str:
    """Return plain text from uploaded file data."""
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        try:
            reader = PdfReader(BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            pass
    elif ext in {".doc", ".docx"}:
        try:
            doc = DocxDocument(BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            pass
    return data.decode("utf-8", errors="ignore")


def analyze_text(prompt: str, text: str, analysis_type: str | None = None) -> str:
    """Send the prompt and text to OpenRouter and return the result."""
    system_prompt = ANALYSIS_PRESETS.get(
        (analysis_type or "").lower(),
        "You are a helpful document analyzer.",
    )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ],
    }
    try:
        response = requests.post(
            OPENROUTER_URL, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as exc:
        raise RuntimeError("Failed to call analysis service") from exc
