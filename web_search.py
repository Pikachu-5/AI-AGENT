import requests

def web_search(query):
    search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(search_url)
        data = response.json()
        print("Raw API response:", data)  # Debug line
        abstract = data.get("AbstractText", "")
        if abstract.strip():
            return abstract
        else:
            return "No relevant information found."
    except Exception as e:
        return f"Error during web search: {e}"
