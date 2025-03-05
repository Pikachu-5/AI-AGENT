# AI-AGENT

## 💡 Overview

```
I Developed an AI agent capable of processing files as input using LangChain. The agent exhibits reasoning capabilities, supports Retrieval-Augmented Generation (RAG), and i implemented function calling for basic arithmetic operations.
```

## 🧮 Key features

```
Arithmetic Module (`arithmetic.py`)

Handles basic arithmetic operations (addition, subtraction, multiplication, division).

File Processor (`file_processor.py`)

Used document loaders (i initially used LlamaIndex, but had issues getting it up and running so later adapted to LangChains DirectoryLoader from the community package) to load text files from the docs folder. It returns a list of document objects that are used for summarization and retrieval.

Notes Summary (`notes_summary.py`)

Reads documents from the docs folder.
Uses regex to extract the target file name from the users input. constructs a prompt and calls the Gemini API(gemini-2.0-flash) to generate a summary of the document.

Reasoning Module (`reasoning.py`)

it gives responses using the Gemini API for queries that do not have the required words.

Web Search (`web_search.py`)

Implements web search functionality. Based on Dduckduckgo.

Retrieval-Augmented Generation (`rag.py`)

Uses LangChain vectorstore and embeddings to index documents for search. This retrieves relevant context from documents to answer user queries more relevantly.

Custom Gemini LLM (`gemini_llm.py`)

This is a custom wrapper to integrate Gemini API with LangChains LLM interface. As mentioned before i was having trouble getting Lama-index running on my sytem, but Langchain doesnt support GEmini API. Therefore i had to do alot of research to create this gemini wrapper that works with langchain.

Web Interface (`templates/index.html`)

The HTML file combines inline CSS for styling and JavaScript (using React and Babel via CDN) to create animated, full-screen chat interface. Added an upload button where the user can input the text tfile to be summarized it and it automatically does it for them.

```

## 🔄 Debugging and Development Journey

```python
- **Initial Setup**  

Started with a cmd chatbot integrating arithmetic operations and basic reasoning. This was relatively easy.

- **Document Summarization:**  
Integrated document ingestion using LlamaIndex first, then migrated to LangChain (with community package imports becuase the import paths are apparently deprecated in  the latest versions of langchain). 
Faced issues with file naming and retrieval so implemented regex-based extraction of file names from user queries.

- **API Integration:**  
Configured the Gmini API by reading the API key from environment variables(used gemini-2.0-flash for testing).

- **Fallback Reasoning:**  
Added a reasoning module to handle queries not caught by arithmetic or summarization.

- **Web Search Transition:**  
Initially started off with Google Custom Search then migrated to DuckDuckGo because of a few API issues. Addressed issues with query cleaning to improve search accuracy.
    
- **UI and Frontend Enhancements:**  
I had some extra time so i created an HTML web-based interface using Flask and React. Added animations using react.
    
- **Final Debugging:**  
Lots and lots of debugging later verified that all functionalities i.e. arithmetic, summarization, web search, reasoning,rag work as expected.

```

## 🔍 Folder Structure

```
ai-agent/ 
├── app.py 
├── arithmetic.py 
├── file_processor.py
├── notes_summary.py
├── reasoning.py
├── web_search.py
├── rag.py 
├── gemini_llm.py
├── uploads/
├── templates/ 
│ └── index.html
```

## 📊 Setup and Installation

```
# Clone or Create the Project Folder:
	Ensure your project foldercontains all the files listed.

# install these dependensies:
	Flask 
	google-generativeai 
	langchain 
	langchain-community 
	
# set env variables:
	GEMINI_API_KEY = yourkey
```

## ⚠️ How to run

```
python app.py 
```
