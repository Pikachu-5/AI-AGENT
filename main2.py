import os
import re
from typing import Optional
import requests
import google.generativeai as genai
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun, Tool
from langchain import hub
from langchain_google_genai import GoogleGenerativeAI

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

llm = GoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

class CachedVectorStore:
    _vectorstore = None

    @classmethod
    def get_vectorstore(cls):
        if cls._vectorstore is None:
            docs = DirectoryLoader("docs", glob="*.txt", loader_cls=TextLoader).load()
            embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")
            cls._vectorstore = FAISS.from_documents(docs, embeddings)
        return cls._vectorstore

def document_retriever(query: str) -> str:
    try:
        vectorstore = CachedVectorStore.get_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)
        
        if not docs:
            return "No relevant documents found in the knowledge base."
            
        context = "\n".join([d.page_content for d in docs])
        response = llm.invoke(
            f"Answer the question based on the following context:\n\n{context}\n\n"
            f"Question: {query}\nAnswer:"
        )
        return response
    except Exception as e:
        return f"Document retrieval error: {str(e)}"

def notes_generator(query: str) -> str:
    try:
        response = llm.invoke(
            f"Convert the following input into well-organized notes with key points and bullet points:\n\n{query}"
        )
        return response
    except Exception as e:
        return f"Notes generation error: {str(e)}"

def calculator(query: str) -> str:
    try:
        expression = re.sub(r"[^\d\+\-\*\/\(\)\.]", "", query)
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {str(e)}"

tools = [
    Tool(
        name="Document Search",
        func=document_retriever,
        description="Useful for answering questions about documents in the knowledge base"
    ),
    Tool(
        name="Web Search",
        func=DuckDuckGoSearchRun(),
        description="Useful for answering questions about current events or real-time information"
    ),
    Tool(
        name="Notes Generator",
        func=notes_generator,
        description="Useful for converting information into structured notes with bullet points"
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for performing mathematical calculations"
    )
]


agent_prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


if __name__ == "__main__":
    while True:
        user_input = input("\nAsk me something (type 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent_executor.invoke({"input": user_input})
        print("\n", response["output"])
