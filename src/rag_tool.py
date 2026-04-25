import os
import pathlib
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CHROMA_DIR = str(BASE_DIR / "chroma_db")

def load_vectorstore():
    """Load the existing ChromaDB knowledge base."""
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

def search_hcc_knowledge(query: str, k: int = 3) -> str:
    """
    Search the HCC knowledge base for relevant conditions.
    Returns formatted clinical context for the agent.
    """
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "No relevant HCC information found."

    response = f"HCC Knowledge Base Results for: '{query}'\n"
    response += "=" * 50 + "\n"

    for i, doc in enumerate(results, 1):
        response += f"\nResult {i}:\n{doc.page_content}\n"
        response += "-" * 30 + "\n"

    return response

def get_related_hccs(condition_name: str) -> str:
    """
    Find HCC conditions clinically related to a given condition.
    Used by the agent to identify potential coding gaps.
    """
    vectorstore = load_vectorstore()

    queries = [
        f"conditions related to {condition_name}",
        f"complications of {condition_name}",
        f"HCC codes associated with {condition_name}"
    ]

    all_results = []
    seen_content = set()

    for query in queries:
        results = vectorstore.similarity_search(query, k=2)
        for doc in results:
            if doc.page_content not in seen_content:
                seen_content.add(doc.page_content)
                all_results.append(doc)

    if not all_results:
        return f"No related HCC conditions found for: {condition_name}"

    response = f"HCC conditions clinically related to {condition_name}:\n"
    response += "=" * 50 + "\n"

    for i, doc in enumerate(all_results[:4], 1):
        response += f"\nRelated Condition {i}:\n{doc.page_content}\n"
        response += "-" * 30 + "\n"

    return response


# ── Test both functions ───────────────────────────────
if __name__ == "__main__":
    print("TEST 1: Search for diabetes-related HCCs")
    print("=" * 55)
    print(search_hcc_knowledge("diabetes complications"))

    print("\nTEST 2: Find conditions related to heart failure")
    print("=" * 55)
    print(get_related_hccs("Congestive Heart Failure"))

    print("\nTEST 3: Search for kidney disease HCCs")
    print("=" * 55)
    print(search_hcc_knowledge("chronic kidney disease stages"))