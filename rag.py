import os
from file_processor import load_documents
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from gemini_llm import GeminiLLM
from langchain.chains import RetrievalQA

def create_vectorstore():
    docs = load_documents("docs")
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def retrieve_info(query):
    vectorstore = create_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = GeminiLLM(model_name="models/gemini-2.0-flash")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa_chain.run(query)
