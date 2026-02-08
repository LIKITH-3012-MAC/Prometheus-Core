import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

# 1. LOAD: చదవడం
# Put your classroom PDF in the same folder
loader = PyPDFLoader("classroom_notes.pdf")
docs = loader.load()

# 2. SPLIT: ముక్కలు చేయడం
# We split long text into 1000-character chunks so the AI can "digest" it easily.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 3. EMBED & STORE: దాచుకోవడం
# Turning text into numbers and saving them in ChromaDB.
# PersistentClient ensures it stays on your disk.
vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chroma_db"
)

# 4. RETRIEVE & ASK: వెతకడం మరియు అడగడం
def ask_prometheus(question):
    # Search the PDF for the most relevant parts
    docs = vectorstore.similarity_search(question)
    context = "\n".join([d.page_content for d in docs])
    
    # Send the context + question to your custom Prometheus model
    llm = Ollama(model="prometheus-ai") 
    prompt = f"Using this context: {context}\n\nQuestion: {question}"
    
    return llm.invoke(prompt)

# Example use:
print(ask_prometheus("What is the main topic of the first chapter?"))
