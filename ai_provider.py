import os

from google import genai
from groq import Groq


# Models
GEMINI_MODEL = "gemini-3.6-flash"
GROQ_MODEL = "openai/gpt-oss-120b"


def ask_gemini(prompt):
    """
    Send a prompt to Gemini.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response")

    return response.text


def ask_groq(prompt):
    """
    Send a prompt to Groq.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("Groq returned an empty response")

    return content


def ask_ai(prompt):
    """
    Common AI interface used by all agents.

    Provider order:
        1. Gemini
        2. Groq fallback
    """

    gemini_available = bool(os.getenv("GEMINI_API_KEY"))
    groq_available = bool(os.getenv("GROQ_API_KEY"))

    if not gemini_available and not groq_available:
        raise RuntimeError(
            "No AI provider configured. "
            "Set GEMINI_API_KEY or GROQ_API_KEY."
        )

    # --------------------------------------------------
    # Primary provider: Gemini
    # --------------------------------------------------

    if gemini_available:
        try:
            print("AI Provider: Gemini")
            return ask_gemini(prompt)

        except Exception as error:
            print(f"Gemini failed: {error}")

            if groq_available:
                print("Falling back to Groq...")

    # --------------------------------------------------
    # Fallback provider: Groq
    # --------------------------------------------------

    if groq_available:
        try:
            print("AI Provider: Groq")
            return ask_groq(prompt)

        except Exception as error:
            print(f"Groq failed: {error}")

            raise RuntimeError(
                "All configured AI providers failed."
            ) from error

    raise RuntimeError("Gemini failed and Groq is not configured.")