import os
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
DB_DIR = "./chroma_db"
MODEL_NAME = "prometheus-ai"

# 1. Load Embeddings and Model
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model=MODEL_NAME)

# 2. Setup Database
if not os.path.exists(DB_DIR):
    print("📥 Loading PDF into Knowledge Base...")
    loader = PyPDFLoader("classroom_notes.pdf")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
else:
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

print(f"\n✅ PROMETHEUS ONLINE. Ask me anything about your notes.\n")

while True:
    query = input("USER: ")
    if query.lower() in ['exit', 'quit']: break
    
    # Retrieval
    results = vectorstore.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in results])
    
    # Generation
    prompt = f"Context: {context}\n\nQuestion: {query}\nAnswer as Prometheus:"
    
    print("\nPROMETHEUS: ", end="")
    for chunk in llm.stream(prompt):
        print(chunk, end="", flush=True)
    print("\n")
