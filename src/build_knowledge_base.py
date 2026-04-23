import os
import pathlib
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "hcc_descriptions.txt"
CHROMA_DIR = str(BASE_DIR / "chroma_db")

print(f"Looking for file at: {DATA_FILE}")
print(f"File exists: {DATA_FILE.exists()}")

if not DATA_FILE.exists():
    print("ERROR: File not found. Run Step 2 above first.")
    exit(1)

print("\nStep 1: Loading HCC reference documents...")
loader = TextLoader(str(DATA_FILE))
documents = loader.load()
print(f"Loaded {len(documents)} document(s)")

print("\nStep 2: Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n\n", "\n", " "]
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

print("\nStep 3: Creating embeddings and storing in ChromaDB...")
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)
print(f"Stored {len(chunks)} chunks in ChromaDB at: {CHROMA_DIR}")

print("\nStep 4: Testing search query...")
results = vectorstore.similarity_search(
    "What HCC codes relate to diabetes?", k=3
)
print("\nSearch results for 'diabetes':")
print("-" * 40)
for i, doc in enumerate(results, 1):
    print(f"\nResult {i}:\n{doc.page_content}")

print("\nKnowledge base built successfully!")