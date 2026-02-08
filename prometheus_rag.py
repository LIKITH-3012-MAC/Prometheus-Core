import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama

# 1. Check if PDF exists
pdf_path = "classroom_notes.pdf"
if not os.path.exists(pdf_path):
    print(f"Error: Please put a PDF named '{pdf_path}' in this folder!")
    exit()

print("Processing your PDF... please wait.")

# 2. LOAD & SPLIT
loader = PyPDFLoader(pdf_path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# 3. EMBED & STORE (Using the nomic model you just pulled)
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")

print("Database ready! Asking Prometheus...")

# 4. ASK THE MODEL
def ask_prometheus(question):
    docs = vectorstore.similarity_search(question)
    context = "\n".join([d.page_content for d in docs])
    llm = Ollama(model="prometheus-ai") 
    prompt = f"Context from PDF:\n{context}\n\nQuestion: {question}\nAnswer as Prometheus AI:"
    return llm.invoke(prompt)

print("\nResponse:\n", ask_prometheus("Summarize the main points of this document."))
