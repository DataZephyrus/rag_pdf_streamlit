import os
import streamlit as st
from app.models.llm_interface import LLMInterface
from app.utils.data_processing import process_uploaded_file
from app.components.chatbot_ui import display_chat_container, clear_chat_history
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    openai_api_key = st.text_input(
        "OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password"
    )

    # Openlayer settings
    st.subheader("Openlayer Settings")
    openlayer_api_key = st.text_input(
        "Openlayer API Key", value=os.getenv("OPENLAYER_API_KEY", ""), type="password"
    )
    openlayer_pipeline_id = st.text_input(
        "Openlayer Pipeline ID", value=os.getenv("YOUR_INFERENCE_PIPELINE_ID", "")
    )

    # Set environment variables from UI inputs
    if openlayer_api_key:
        os.environ["OPENLAYER_API_KEY"] = openlayer_api_key
    if openlayer_pipeline_id:
        os.environ["OPENLAYER_INFERENCE_PIPELINE_ID"] = openlayer_pipeline_id

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
