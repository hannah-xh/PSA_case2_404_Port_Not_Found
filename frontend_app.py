import streamlit as st
import pandas as pd
from powerbi_connector import PowerBIConnector
from decision_engine import DecisionEngine
from conversation_manager import ConversationManager
from evaluation_system import EvaluationSystem
from llm_client import LLMClient

st.set_page_config(
    page_title="PSA Intelligent Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def initialize_components():
    pbi = PowerBIConnector()
    engine = DecisionEngine()
    conv_mgr = ConversationManager()
    eval_sys = EvaluationSystem()
    llm = LLMClient()
    return pbi, engine, conv_mgr, eval_sys, llm

pbi, engine, conv_mgr, eval_sys, llm = initialize_components()

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = None

st.title("PSA Intelligent Assistant")
st.caption("AI-Powered Global Insights Dashboard")

with st.sidebar:
    st.header("Configuration")
    
    strategy = st.selectbox(
        "Strategy Priority",
        ["balanced", "carbon_reduction", "cost_efficiency", "reliability"]
    )
    
    from config import decision_weights
    engine.weights = decision_weights.update_for_strategy(strategy)
    
    st.divider()
    
    st.header("Performance Metrics")
    metrics = eval_sys.get_real_time_metrics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", metrics['queries_this_session'])
        st.metric("Avg Response", f"{metrics['last_10_avg_response']}s")
    with col2:
        st.metric("Time Saved", f"{metrics['estimated_time_saved']}min")
        
        if metrics['queries_this_session'] > 0 and metrics['last_10_avg_response'] > 0:
            speedup = round(300 / metrics['last_10_avg_response'], 1)
            st.metric("Speedup", f"{speedup}x")
        else:
            st.metric("Speedup", "N/A")
    
    st.divider()
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        conv_mgr.clear_context()
        st.rerun()
    
    if st.button("Refresh Data"):
        st.session_state.data_cache = None
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "metrics" in message:
            with st.expander("Performance Details"):
                st.json(message["metrics"])

if prompt := st.chat_input("Ask about operations, performance, or get recommendations..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        start_time = eval_sys.start_query()
        
        try:
            intent = conv_mgr.infer_intent(prompt)
            
            if st.session_state.data_cache is None:
                with st.spinner("Fetching data from Power BI..."):
                    st.session_state.data_cache = pbi.get_operator_data()
            
            df = st.session_state.data_cache
            
            if intent['entities']['operators']:
                operators = intent['entities']['operators']
                df_filtered = df[df['Operator'].isin(operators)]
            else:
                df_filtered = df
            
            if intent['type'] == 'comparison' and len(intent['entities']['operators']) >= 2:
                comparison = engine.compare_operators(df, intent['entities']['operators'])
                data_summary = f"Operator Comparison:\n{comparison}"
            elif intent['type'] == 'ranking':
                top_performers = engine.get_top_performers(df_filtered)
                data_summary = f"Top Performers:\n{top_performers.to_string()}"
            else:
                analyzed = engine.analyze_dataframe(df_filtered.head(50))
                stats = {
                    'total_vessels': len(analyzed),
                    'avg_dis': round(analyzed['DIS_Score'].mean(), 2),
                    'avg_wait_time': round(analyzed['Wait Time (Hours): ATB-BTR'].mean(), 2),
                    'total_bunker_saved': round(analyzed['Bunker Saved (USD)'].sum(), 2),
                    'on_time_rate': round((analyzed['Arrival Accuracy (Final BTR)'] == 'Y').mean() * 100, 1)
                }
                data_summary = f"Analysis Summary:\n{stats}"
            
            full_prompt = conv_mgr.build_prompt(prompt, data_summary)
            
            response = llm.generate_response(
                full_prompt,
                system_message="You are a maritime operations analyst for PSA International. Provide clear, data-driven insights."
            )
            
            if response['success']:
                answer = response['content']
            else:
                answer = "Unable to generate response. Please try again."
            
            recommendations = engine.generate_recommendations(df_filtered)
            
            full_response = f"{answer}\n\n**Recommendations:**\n"
            for i, rec in enumerate(recommendations[:3], 1):
                full_response += f"{i}. {rec}\n"
            
            message_placeholder.markdown(full_response)
            
            response_time = eval_sys.end_query(start_time)
            
            quality = eval_sys.evaluate_answer_quality(
                answer,
                has_metrics='avg' in answer.lower() or 'total' in answer.lower(),
                has_recommendations=len(recommendations) > 0
            )
            
            performance_data = {
                'response_time': round(response_time, 2),
                'quality_score': quality['quality_score'],
                'tokens_used': response.get('tokens_used', 0),
                'speedup_vs_manual': eval_sys.calculate_speedup(response_time)
            }
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "metrics": performance_data
            })
            
            conv_mgr.add_message("user", prompt)
            conv_mgr.add_message("assistant", answer)
            
            st.rerun()
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.rerun()

with st.expander("Sample Questions"):
    st.markdown("""
    - Compare GRN and NVX operator performance
    - Show top 5 vessels by efficiency
    - What are the main delay factors?
    - Which operators have best carbon performance?
    - Recommend improvements for wait time reduction
    """)