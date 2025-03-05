from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(directory: str):
    loader = DirectoryLoader(directory, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

if __name__ == "__main__":
    docs = load_documents("docs")
    for i, doc in enumerate(docs, start=1):
        print(f"Document {i}:")
        print(doc.page_content[:200])
