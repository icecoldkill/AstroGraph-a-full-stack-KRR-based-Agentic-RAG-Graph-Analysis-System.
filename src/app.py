import streamlit as st
import os
from graph_rag_engine import GraphRAGEngine
import pandas as pd
from rdflib import Graph
import matplotlib.pyplot as plt
import networkx as nx

# Page Config
st.set_page_config(page_title="Space Exploration Knowledge Graph", layout="wide")

# Theme / CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-bubble { background-color: #1e2a3a; }
    .bot-bubble { background-color: #2e3b4a; border-left: 5px solid #4CAF50; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🚀 Space Explorer KG")
groq_key = st.sidebar.text_input("Enter Groq API Key", type="password")
uploaded_files = st.sidebar.file_uploader("Upload Documents (CSV/Txt)", accept_multiple_files=True)

if not groq_key:
    st.warning("Please enter your Groq API key to proceed.")
    st.stop()

# Initialize Engine
@st.cache_resource
def get_engine(api_key):
    return GraphRAGEngine(api_key, "data/space_data.rdf")

engine = get_engine(groq_key)

if uploaded_files:
    save_paths = []
    for f in uploaded_files:
        path = os.path.join("data", f.name)
        with open(path, "wb") as buffer:
            buffer.write(f.getbuffer())
        save_paths.append(path)
    engine.add_documents(save_paths)
    st.sidebar.success(f"Loaded {len(uploaded_files)} files!")

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Agent Chat", "📊 Data Overview", "🕸️ Graph Visualizer"])

with tab1:
    st.subheader("Agentic GraphRAG Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        role_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        st.markdown(f'<div class="chat-bubble {role_class}"><b>{msg["role"].upper()}:</b> {msg["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about space missions, agencies, or budgets..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("AI is thinking and querying the Knowledge Graph..."):
            response = engine.get_agent_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

with tab2:
    st.subheader("Raw Knowledge Graph Data")
    df = pd.read_csv("data/space_missions.csv")
    st.dataframe(df.style.highlight_max(axis=0))

with tab3:
    st.subheader("Interactive Graph Analysis")
    if st.button("Generate Graph Sample"):
        G = nx.Graph()
        # Add a few representative triples from the graph
        for s, p, o in engine.g:
            if "mission" in str(s) or "agency" in str(s):
                s_label = str(s).split("/")[-1]
                o_label = str(o).split("/")[-1]
                p_label = str(p).split("#")[-1] if "#" in str(p) else str(p).split("/")[-1]
                G.add_edge(s_label, o_label, label=p_label)
            if len(G.edges()) > 30: break
        
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_cmap=plt.cm.Blues, font_size=8)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
        st.pyplot(plt)
