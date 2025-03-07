import re
import google.generativeai as genai
import os
from file_processor import load_documents

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
genai.configure(api_key=api_key)

def generate_summary(query):
    match = re.search(r"summarize(?: the document| the file)?(?: on| for)?\s+([\w\-.]+)", query)
    
    if match:
        file_name = match.group(1)
        docs = load_documents("docs")
        target_doc = None
        for doc in docs:
            if file_name.lower() in doc.metadata.get("source", "").lower():
                target_doc = doc
                break
        if not target_doc:
            return f"Could not find a document containing '{file_name}' in its name in the docs folder."
        prompt = f"Summarize the following document:\n\n{target_doc.page_content}"
    else:
        prompt = f"Summarize the following text:\n\n{query}"

    try:
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"Error generating summary: {e}"
