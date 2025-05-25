import streamlit as st
import sys
import os
from datetime import datetime
import logging

# Setup paths and logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.router_agent import router_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Enterprise AI Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: 2rem; }
    .result-box { background-color: #222222; padding: 0.5rem; border-radius: 5px; font-family: monospace; border: 1px solid #ccc; }
    .sql-box { background-color: #f0f0f0; padding: 0.5rem; border-radius: 5px; font-family: monospace; border: 1px solid #ccc; }
    .error-box { background-color: #ffe6e6; padding: 1rem; border-radius: 10px; border-left: 4px solid #ff4444; }
    .history-item { background-color: #f9f9f9; padding: 0.75rem; border-radius: 8px; border-left: 4px solid #6c757d; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

def log_query(entry: dict):
    entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.query_history.append(entry)

def main():
    initialize_session_state()
    
    st.markdown('<h1 class="main-header">🔍 Enterprise AI Search</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("🛠️ Options")
        st.checkbox("Show Generated SQL", key="show_sql", value=True)

        st.header("📝 Sample Queries")
        sample_queries = [
            "How many customers ordered food more than $30 in total?",
            "Return the top 5 customers based on total order amount",
            "What is the total revenue for the company?",
        ]
        for q in sample_queries:
            if st.button(q, key=q):
                st.session_state.current_query = q

    query = st.text_input(
        "Ask something about your enterprise data:",
        placeholder="e.g., Which customer ordered most in Jan?",
        value=st.session_state.get('current_query', ''),
        key="query_input"
    )

    if st.button("🔍 Search", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Processing your query..."):
                result_obj = router_agent(query)

                # 📊 Result
                st.markdown("### 🟩 Answer")
                if isinstance(result_obj['output'], str) and result_obj['output'].lower().startswith("error"):
                    st.markdown(f"<div class='error-box'>❌ {result_obj['output']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='result-box'>{result_obj['output']}</div>", unsafe_allow_html=True)

                # 🗄️ SQL (optional)
                if result_obj.get('sql') and st.session_state.show_sql:
                    st.markdown("### 🟦 Generated SQL Query")
                    st.code(result_obj['sql'], language="sql")

                log_query(result_obj)
        else:
            st.warning("Please enter a query to search.")
    
    # 📋 History
    if st.session_state.query_history:
        st.markdown("---")
        st.header("📋 Recent Queries")
        for entry in reversed(st.session_state.query_history[-5:]):
            with st.expander(f"🔹 {entry['question'][:60]}"):
                st.markdown("**🟩 Answer:**")
                st.markdown(f"<div class='result-box'>{entry['output']}</div>", unsafe_allow_html=True)
                if entry.get('sql') and st.session_state.show_sql:
                    st.markdown("**🟦 SQL:**")
                    st.code(entry['sql'], language="sql")

if __name__ == "__main__":
    main()
