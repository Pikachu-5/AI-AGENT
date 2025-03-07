import os
import re
from arithmetic import call_function
from notes_summary import generate_summary
from web_search import web_search
from reasoning import infer_reasoning 
from rag import retrieve_info

def process_query(query):
    query = query.lower().strip()

    if query.startswith("upload "):
        filename = query[7:].strip()
        if not os.path.exists(filename):
            return f"File '{filename}' not found."
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return generate_summary(content)
        except Exception as e:
            return f"Error reading file: {e}"    

    # arithmetic
    math_match = re.match(r"(\d+)\s*([\+\-\*/])\s*(\d+)", query)
    if math_match:
        a, operator, b = int(math_match.group(1)), math_match.group(2), int(math_match.group(3))
        op_map = {"+": "add", "-": "subtract", "*": "multiply", "/": "divide"}
        return call_function(op_map[operator], a, b)
    tokens = query.split()
    if tokens[0] in ["add", "subtract", "multiply", "divide"] and len(tokens) == 3:
        a, b = int(tokens[1]), int(tokens[2])
        return call_function(tokens[0], a, b)

    # summary
    if "summarize" in query or "notes" in query:
        return generate_summary(query)

    # websearch
    if "search" in query:
        clean_query = query.replace("search", "").strip()
        if clean_query.startswith("for "):
            clean_query = clean_query[4:].strip()
        return web_search(clean_query)
    # rag
    if "document" in query or "file" in query:
        return retrieve_info(query)
    
    return infer_reasoning(query)

if __name__ == "__main__":
    while True:
        user_input = input("Ask me something: ")
        if user_input.lower() == "exit":
            break
        print(process_query(user_input))
