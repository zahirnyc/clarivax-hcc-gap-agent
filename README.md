# 🏥 Clarivax HCC Gap Intelligence Agent

> AI-powered Medicare HCC coding gap identification system  
> Built by [Zahirul Islam](https://linkedin.com/in/zahir-islam) | [Clarivax Analytics](https://clarivexanalytics.com)

---

## What This Does

The Clarivax HCC Gap Intelligence Agent automatically identifies 
Medicare HCC coding gaps for Medicare Advantage populations — a 
process that typically requires expensive manual chart review teams.

Given a Medicare member population, the agent:
- Queries member condition history from a Snowflake data warehouse
- Searches a clinical HCC knowledge base using RAG (Retrieval-Augmented Generation)
- Identifies suspected coding gaps based on clinical relationships
- Produces prioritized gap closure reports with RAF weight impact

---

## The Business Problem

Medicare Advantage health plans lose millions in uncaptured RAF 
revenue every year due to HCC coding gaps. A single 0.05 RAF score 
improvement across 50,000 members can represent $5–10M in annual 
revenue. Traditional approaches rely on expensive vendor suspecting 
tools or large manual chart review teams.

This agent demonstrates how AI can automate gap identification at 
a fraction of the cost.

---

## Architecture
CMS Medicare Data
│
▼
┌─────────────────┐     ┌──────────────────────┐
│   Snowflake     │     │   ChromaDB (RAG)      │
│  Data Warehouse │     │  HCC Knowledge Base   │
│  (Member HCCs,  │     │  (ICD-10 mappings,    │
│   RAF weights)  │     │   clinical criteria)  │
└────────┬────────┘     └──────────┬───────────┘
│                         │
▼                         ▼
┌────────────────────────────────────┐
│     LangChain Agent + OpenAI       │
│     (ReAct reasoning loop)         │
└────────────────────────────────────┘
│
▼
┌──────────────────┐
│  HCC Gap Report  │
│  with RAF Impact │
└──────────────────┘
---

## Tech Stack

| Layer | Technology |
|---|---|
| AI / LLM | OpenAI GPT-4o-mini |
| Agent Framework | LangChain |
| Vector Store | ChromaDB |
| Data Warehouse | Snowflake |
| Data Processing | Python, Pandas |
| Version Control | GitHub |

---

## Sample Output
QUERY: Analyze member MBR00001. What HCC coding gaps
should we investigate?
FINAL GAP REPORT:
────────────────────────────────────────────────────
Member MBR00001 — Age: 72, Female
CODED CONDITIONS:
HCC 85 — Congestive Heart Failure (RAF: 0.323)
HCC 19 — Diabetes without Complication (RAF: 0.118)
IDENTIFIED CODING GAPS:

HCC 96 — Atrial Fibrillation (RAF: 0.168)
→ Commonly co-occurs with heart failure
→ ICD-10 to query: I48.0, I48.11, I48.19
HCC 136 — Chronic Kidney Disease Stage 5 (RAF: 0.538)
→ Diabetes complication — check lab values
→ ICD-10 to query: N18.5, N18.6
HCC 18 — Diabetes with Chronic Complication (RAF: 0.302)
→ Upgrade from HCC 19 if nephropathy confirmed
→ ICD-10 to query: E11.40, E11.41

ESTIMATED RAF IMPACT IF ALL GAPS CLOSED: +1.008
────────────────────────────────────────────────────
---

## Project Structure
clarivax-hcc-gap-agent/
├── data/
│   ├── hcc_descriptions.txt     # HCC clinical knowledge base
│   └── member_conditions.csv    # Synthetic Medicare member data
├── src/
│   ├── generate_data.py         # Synthetic data generator
│   ├── build_knowledge_base.py  # ChromaDB RAG builder
│   ├── snowflake_tool.py        # Snowflake SQL query tool
│   ├── rag_tool.py              # HCC RAG retrieval tool
│   ├── hcc_gap_agent.py         # Main agent (entry point)
│   └── test_ai.py               # API connection test
├── .env.example                 # Environment variable template
├── requirements.txt             # Python dependencies
└── README.md
---

## Setup Instructions

### Prerequisites
- Python 3.11+
- Snowflake account (free trial at snowflake.com)
- OpenAI API key (platform.openai.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/clarivax-hcc-gap-agent
cd clarivax-hcc-gap-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat      # Windows
source venv/bin/activate        # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your credentials:
OPENAI_API_KEY=your-openai-key
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_DATABASE=CLARIVAX_DB
SNOWFLAKE_SCHEMA=RISK_ADJUSTMENT
### Run the agent

```bash
# Step 1 — Generate synthetic Medicare data
python src/generate_data.py

# Step 2 — Load data into Snowflake
# (Run SQL in snowflake_setup.sql in your Snowflake worksheet)

# Step 3 — Build the HCC knowledge base
python src/build_knowledge_base.py

# Step 4 — Run the gap agent
python src/hcc_gap_agent.py
```

---

## About Clarivax Analytics

Clarivax Analytics helps Medicare Advantage health plans and risk 
adjustment contractors improve HCC capture rates, automate gap 
identification, and connect RAF performance to revenue — using 
Snowflake, AI, and 10+ years of CMS expertise.

**Services:** RA Analytics · AI Automation · Snowflake BI · 
Medicare Data Consulting

🌐 [clarivexanalytics.com](https://clarivexanalytics.com)  
💼 [LinkedIn](https://linkedin.com/in/zahir-islam)  
📧 zahir_usa@hotmail.com

---

## Disclaimer

This project uses synthetic data generated to mirror CMS Medicare 
data structures. No real patient data is used or stored.
