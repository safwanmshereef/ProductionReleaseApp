import json
import importlib
import re
from typing import Any, Dict, List, cast

import streamlit as st

try:
    genai = importlib.import_module("google.generativeai")
except Exception:
    genai = None

DEFAULT_MODEL = "gemini-1.5-flash"


def get_google_api_key() -> str:
    key = ""
    if "GOOGLE_API_KEY" in st.secrets:
        key = (st.secrets.get("GOOGLE_API_KEY") or "").strip()
    if not key and "GEMINI_API_KEY" in st.secrets:
        key = (st.secrets.get("GEMINI_API_KEY") or "").strip()
    return key


def is_gemini_ready() -> bool:
    return bool(genai is not None and get_google_api_key())


def _configure_model(model_name: str = DEFAULT_MODEL, system_instruction: str = ""):
    if genai is None:
        raise RuntimeError(
            "google-generativeai package is not installed. Add it to requirements and reinstall dependencies."
        )

    api_key = get_google_api_key()
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing from Streamlit secrets.")

    genai_client = cast(Any, genai)
    genai_client.configure(api_key=api_key)
    if system_instruction:
        return genai_client.GenerativeModel(model_name, system_instruction=system_instruction)
    return genai_client.GenerativeModel(model_name)


def generate_text(
    prompt: str,
    system_instruction: str = "",
    model_name: str = DEFAULT_MODEL,
    temperature: float = 0.3,
    max_output_tokens: int = 800,
) -> str:
    model = _configure_model(model_name=model_name,
                             system_instruction=system_instruction)
    generation_config = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }
    response = cast(Any, model).generate_content(
        prompt, generation_config=generation_config)
    if hasattr(response, "text") and response.text:
        return response.text.strip()

    candidates = getattr(response, "candidates", None)
    if not candidates:
        return "No response generated."

    chunks: List[str] = []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        if not content:
            continue
        parts = getattr(content, "parts", [])
        for part in parts:
            text_value = getattr(part, "text", "")
            if text_value:
                chunks.append(text_value)

    return "\n".join(chunks).strip() if chunks else "No response generated."


def _extract_json(text: str) -> Dict:
    if not text:
        return {}

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except Exception:
        return {}


def fallback_triage(title: str, description: str) -> Dict[str, str]:
    raw = f"{title} {description}".lower()

    priority = "Medium"
    impact = "Medium"
    category = "Other"
    sentiment = "Neutral"

    if any(token in raw for token in ["down", "outage", "critical", "p1", "urgent"]):
        priority = "Critical"
        impact = "High"
        sentiment = "Urgent"
    elif any(token in raw for token in ["error", "fail", "broken", "issue"]):
        priority = "High"
        impact = "Medium"

    if any(token in raw for token in ["access", "permission", "role", "login"]):
        category = "Access"
    elif any(token in raw for token in ["feature", "enhancement", "improve", "add"]):
        category = "Feature Request"
    elif any(token in raw for token in ["bug", "exception", "trace", "error", "failed"]):
        category = "Bug"

    summary = (
        "Automated triage suggests this ticket should be reviewed by the operations team "
        "and prioritized based on business impact."
    )

    return {
        "priority": priority,
        "category": category,
        "impact": impact,
        "sentiment": sentiment,
        "summary": summary,
    }


def triage_ticket(title: str, description: str) -> Dict[str, str]:
    if not is_gemini_ready():
        return fallback_triage(title, description)

    prompt = f"""
You are an IT service desk triage assistant.
Analyze the ticket title and description and respond as strict JSON only with keys:
priority, category, impact, sentiment, summary.

Allowed values:
priority: Low, Medium, High, Critical
category: Bug, Feature Request, Access, Other
impact: Low, Medium, High
sentiment: Neutral, Concerned, Urgent

Title: {title}
Description: {description}
"""

    try:
        raw = generate_text(
            prompt=prompt,
            system_instruction="Return strict JSON with no markdown.",
            temperature=0.2,
            max_output_tokens=300,
        )
        parsed = _extract_json(raw)
        if not parsed:
            return fallback_triage(title, description)

        return {
            "priority": parsed.get("priority", "Medium"),
            "category": parsed.get("category", "Other"),
            "impact": parsed.get("impact", "Medium"),
            "sentiment": parsed.get("sentiment", "Neutral"),
            "summary": parsed.get("summary", ""),
        }
    except Exception:
        return fallback_triage(title, description)


def answer_with_context(user_prompt: str, context_blob: str, history: List[Dict[str, str]]) -> str:
    if not is_gemini_ready():
        return (
            "Gemini is not configured yet. Add GOOGLE_API_KEY in .streamlit/secrets.toml to enable live AI answers.\n\n"
            "Quick guidance: include key ticket IDs, affected jobs, and expected outcome in your prompt for better help."
        )

    turns = []
    for message in history[-8:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        turns.append(f"{role.upper()}: {content}")
    conversation = "\n".join(turns)

    prompt = f"""
You are an enterprise support assistant for operations and incident response.
Use the provided context to give precise, actionable steps.
When relevant, include: diagnosis, probable cause, next checks, and mitigation plan.
Keep response concise and structured.

Operational Context:
{context_blob}

Conversation So Far:
{conversation}

User Question:
{user_prompt}
"""

    return generate_text(
        prompt=prompt,
        system_instruction="Provide practical, safe, production-focused guidance.",
        temperature=0.35,
        max_output_tokens=900,
    )
