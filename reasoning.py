import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def infer_reasoning(query):

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(query)
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"Error during reasoning: {e}"
