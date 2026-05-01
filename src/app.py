import streamlit as st
import sys, os, pathlib
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
sys.path.append(str(pathlib.Path(__file__).parent))
load_dotenv()
from snowflake_tool import query_member_conditions, find_hcc_gaps, get_population_summary
from rag_tool import search_hcc_knowledge, get_related_hccs
st.set_page_config(page_title="Clarivax HCC Gap Agent", page_icon="🏥", layout="wide")
st.title("🏥 Clarivax HCC Gap Intelligence Agent")
analysis_type = st.selectbox("Analysis Type", ["Single Member Gap Analysis", "Population HCC Summary"])
if analysis_type == "Single Member Gap Analysis":
    member_id = st.text_input("Enter Member ID", placeholder="e.g. MBR00001")
    if st.button("Analyze", type="primary") and member_id:
        with st.spinner("Analyzing..."):
            member_data = query_member_conditions(member_id)
            hcc_context = search_hcc_knowledge("HCC coding gaps")
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
            response = llm.invoke([SystemMessage(content="You are a Medicare RA expert. Identify HCC coding gaps."), HumanMessage(content=f"Analyze:\nMEMBER DATA:\n{member_data}\nHCC CONTEXT:\n{hcc_context}")])
        st.markdown(response.content)
elif analysis_type == "Population HCC Summary":
    if st.button("Run Analysis", type="primary"):
        with st.spinner("Querying Snowflake..."):
            pop_data = get_population_summary()
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
            response = llm.invoke([SystemMessage(content="You are a Medicare RA expert."), HumanMessage(content=f"Summarize this population data:\n{pop_data}")])
        st.markdown(response.content)
