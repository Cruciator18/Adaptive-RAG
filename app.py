import streamlit as st
from graph import app # Ensure this points to your compiled LangGraph


st.set_page_config(page_title="Adaptive RAG Agent", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Hide the default Streamlit top padding */
    .block-container { padding-top: 2rem; }
    
    /* Header Layout */
    .header-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .title-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        color: #111827; /* Darker, sophisticated text */
    }
    .subtitle {
        color: #6B7280; /* Darker grey for readability */
        font-size: 1.05rem;
        margin-top: -5px;
        margin-bottom: 20px;
    }
    
    /* Document Status Indicator */
    .doc-status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #F3F4F6;
        color: #4B5563;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #E5E7EB;
        margin-bottom: 30px;
    }

    /* 4. Enhance the Input Area */
    /* Target the container wrapping the chat input */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
        padding-right: 5px !important; /* Make room for the colored button */
    }
    
    /* Highlight the Submit Button inside the input box */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #1E3A8A !important; /* Deep Blue CTA */
        color: white !important;
        border-radius: 8px !important;
    }
    /* Force the arrow icon to be white */
    [data-testid="stChatInputSubmitButton"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-wrapper">
    <div class="title-wrapper">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
        </svg>
        <h1 class="main-title">Adaptive RAG Agent</h1>
    </div>
    <a href="#" style="color: #9CA3AF;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
        </svg>
    </a>
</div>
<p class="subtitle">Ask questions based on the ingested documents. The agent will route, grade, and self-correct.</p>
<div class="doc-status">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
    </svg>
    <span>Currently referencing: <strong>sample_report.pdf</strong></span>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


active_prompt = None

if len(st.session_state.messages) == 0:
    st.write(" Get started")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Summarize the document", use_container_width=True):
            active_prompt = "Can you provide a comprehensive summary of the referenced document?"
    with col2:
        if st.button("🔑 What are the key points?", use_container_width=True):
            active_prompt = "What are the core methodologies or key points discussed in the text?"
    with col3:
        if st.button("🌐 Search latest news", use_container_width=True):
            active_prompt = "Search the web for the latest news regarding this topic."
            
    st.markdown("<br>", unsafe_allow_html=True) # Spacer

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


chat_bar_input = st.chat_input("Ask a question about the document...")

if chat_bar_input:
    active_prompt = chat_bar_input

if active_prompt:
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    
    with st.chat_message("assistant"):
        with st.status("Agent is thinking...", expanded=True) as status_box:
            initial_state = {"question": active_prompt, "search_count": 0}
            final_generation = ""
            
            for output in app.stream(initial_state):
                for node_name, state_data in output.items():
                    st.write(f"🔄 Executed Node: **{node_name}**")
                    if "generation" in state_data:
                        final_generation = state_data["generation"]
            
            status_box.update(label="Response generated!", state="complete", expanded=False)
        
        # Display the final answer
        st.markdown(final_generation)
        st.session_state.messages.append({"role": "assistant", "content": final_generation})
        
        
        st.rerun()