import os
import sys
import pathlib
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

sys.path.append(str(pathlib.Path(__file__).parent))

from snowflake_tool import (
    query_member_conditions,
    find_hcc_gaps,
    get_population_summary
)
from rag_tool import (
    search_hcc_knowledge,
    get_related_hccs
)

load_dotenv()

# ── System prompt ─────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Medicare Risk 
Adjustment analyst at Clarivax Analytics. You identify 
HCC coding gaps for Medicare Advantage members.

When analyzing a member:
1. Review their coded conditions
2. Identify clinically related conditions that may be 
   missing (coding gaps)
3. Prioritize gaps by RAF weight impact
4. Provide a clear, actionable gap report

Always be specific about HCC codes, ICD-10 codes, 
and RAF weights in your recommendations."""

# ── Core agent function ───────────────────────────────

def run_gap_analysis(query: str) -> str:
    """
    Run HCC gap analysis using LLM + direct tool calls.
    This approach works with all LangChain versions.
    """
    print("\n" + "=" * 60)
    print(f"QUERY: {query.strip()}")
    print("=" * 60)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Step 1 — get population context
    print("\nStep 1: Fetching population data from Snowflake...")
    population_data = get_population_summary()

    # Step 2 — get member data if member ID in query
    member_data = ""
    for word in query.split():
        if word.startswith("MBR"):
            print(f"Step 2: Looking up member {word}...")
            member_data = query_member_conditions(word)
            break

    # Step 3 — search HCC knowledge base
    print("Step 3: Searching HCC knowledge base...")
    hcc_context = search_hcc_knowledge(query)

    # Step 4 — get related conditions
    print("Step 4: Finding related HCC conditions...")
    related = ""
    if "diabetes" in query.lower() or "Diabetes" in query:
        related += get_related_hccs("Diabetes")
    if "heart" in query.lower():
        related += get_related_hccs("Congestive Heart Failure")
    if "kidney" in query.lower() or "ckd" in query.lower():
        related += get_related_hccs("Chronic Kidney Disease")
    if not related:
        related = get_related_hccs(query.split()[0])

    # Step 5 — build context for LLM
    full_context = f"""
POPULATION SUMMARY:
{population_data}

MEMBER DATA:
{member_data if member_data else 'No specific member requested'}

HCC KNOWLEDGE BASE:
{hcc_context}

RELATED CONDITIONS:
{related}
"""

    # Step 6 — generate gap report with LLM
    print("Step 5: Generating gap analysis report...\n")
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""
Using the data below, answer this query and provide 
a detailed HCC gap analysis report:

QUERY: {query}

DATA:
{full_context}

Provide:
1. Summary of coded conditions found
2. Identified HCC coding gaps with HCC codes
3. ICD-10 codes to look for in chart review
4. RAF weight impact of each gap
5. Priority order for gap closure outreach
""")
    ]

    response = llm.invoke(messages)

    print("FINAL GAP REPORT:")
    print("-" * 60)
    print(response.content)
    return response.content


# ── Main ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  CLARIVAX HCC GAP INTELLIGENCE AGENT")
    print("  Powered by OpenAI + Snowflake + ChromaDB")
    print("=" * 60)

    # Query 1 — single member analysis
    run_gap_analysis("""
        Analyze member MBR00001. What HCC conditions 
        do they have? What coding gaps should we 
        investigate?
    """)

    # Query 2 — diabetes gap analysis
    run_gap_analysis("""
        Find members with Diabetes. What related 
        conditions like Diabetic Nephropathy or CKD 
        are common coding gaps we should prioritize?
    """)

    # Query 3 — executive summary
    run_gap_analysis("""
        Give me an executive summary of our Medicare 
        population. Which HCC conditions should we 
        prioritize for gap closure outreach based on 
        RAF weight and member volume?
    """)