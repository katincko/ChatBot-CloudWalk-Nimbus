import os
from dotenv import load_dotenv 
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()
DATA_PATH = "data/"
DB_FAISS_PATH = "vector_store/"

def main():
    print("Ingesting data...🤓")
    # Carrega os documentos do diretório especificado
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")
    docs = loader.load()
    print(f"Carregados {len(docs)} documentos.")

    # Divide os documentos em pedaços menores
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"Divididos em {len(splits)} pedaços.")

    # Cria os embeddings para os pedaços de texto
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("Criando embeddings...")

    #Banco de dados vetorial FAISS
    db = FAISS.from_documents(splits, embeddings)
    print("Banco de dados vetorial criado.")

    # Salva o banco de dados vetorial no disco
    db.save_local(DB_FAISS_PATH)
    print(f"✅ Banco de dados salvo com sucesso na pasta: {DB_FAISS_PATH}")
    

if __name__ == "__main__":
    main()