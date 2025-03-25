import streamlit as st
from app.models.llm_interface import LLMInterface
from app.utils.data_processing import process_uploaded_file
from app.components.chatbot_ui import display_chat_container, clear_chat_history

# Page configuration
st.set_page_config(page_title="PDF Chat Assistant", page_icon="📄", layout="wide")

# Application header
st.title("📄 PDF Chat Assistant")
st.markdown("### Upload your PDF and chat with its contents")

# Sidebar
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    st.markdown("---")
    st.subheader("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    clear_button = st.button("Clear Chat History")

# Main chat interface
if clear_button:
    clear_chat_history()

if uploaded_file is not None:
    documents = process_uploaded_file(uploaded_file)
    if documents:
        try:
            llm = LLMInterface(openai_api_key)
            if llm.initialize_retrieval_chain(documents):
                display_chat_container(llm)
            else:
                st.error("Failed to initialize LLM. Check your API key and document.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Could not process the uploaded PDF. Please try a different file.")
else:
    st.info("👈 Please upload a PDF document from the sidebar to get started.")

