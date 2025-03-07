from langchain.llms.base import LLM
from typing import Optional, List
import google.generativeai as genai
import os

class GeminiLLM(LLM):
    model_name: str = "models/gemini-2.0-flash"

    @property
    def _llm_type(self) -> str:
        return "google_gemini"

    def __init__(self, model_name: str = None, **kwargs):
        super().__init__(**kwargs)
        if model_name is not None:
            self.model_name = model_name
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        genai.configure(api_key=api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            return f"Error calling Gemini: {e}"
