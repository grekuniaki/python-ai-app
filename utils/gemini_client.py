import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)


class GeminiConfigError(Exception):
    """Raised when required configuration (e.g. GEMINI_API_KEY) is missing."""
    pass


class GeminiAPIError(Exception):
    """Raised when the Gemini API call itself fails (network, quota, invalid request, etc.)."""
    pass


def get_model_name() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


@st.cache_resource
def _get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiConfigError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
    return genai.Client(api_key=api_key)


def generate_text(
    user_prompt: str,
    system_instruction: str | None = None,
    temperature: float = 0.7,
) -> str:
    """Send one prompt to Gemini and return response.text.
    Raises GeminiConfigError if the API key is missing.
    Raises GeminiAPIError if the call fails or returns an empty response.
    """
    try:
        client = _get_client()
    except GeminiConfigError:
        raise

    model = get_model_name()

    try:
        from google.genai import types

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=config,
        )

        if not response.text or response.text.strip() == "":
            raise GeminiAPIError("Gemini から空の応答が返されました。")

        return response.text

    except GeminiConfigError:
        raise
    except GeminiAPIError:
        raise
    except Exception as exc:
        raise GeminiAPIError(f"API 呼び出しエラー: {str(exc)}")
