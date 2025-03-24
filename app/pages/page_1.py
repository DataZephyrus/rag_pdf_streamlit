# rag_pdf_streamlit/app/pages/page_1.py
import streamlit as st
from app.components.chatbot_ui import display_chat_container, clear_chat_history
from app.utils.data_processing import process_uploaded_file
from app.models.llm_interface import LLMInterface


def pdf_chat_page():
    st.title("Chat with your PDF")

    # Sidebar content
    with st.sidebar:
        st.header("Document Settings")

        # File upload widget
        uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

        # Clear chat button
        if st.button("Clear Chat"):
            clear_chat_history()

            # Also reset the LLM interface
            if "llm_interface" in st.session_state:
                st.session_state.llm_interface.reset()
            st.rerun()

    # Initialize LLM interface
    if "llm_interface" not in st.session_state:
        st.session_state.llm_interface = LLMInterface()

    # Process uploaded file
    if uploaded_file:
        if (
            "current_file" not in st.session_state
            or st.session_state.current_file != uploaded_file.name
        ):
            with st.spinner("Processing document..."):
                # Extract text from the PDF
                text_content = process_uploaded_file(uploaded_file)

                if text_content:
                    # Initialize the retrieval chain
                    st.session_state.llm_interface.initialize_retrieval_chain(
                        text_content
                    )
                    st.session_state.current_file = uploaded_file.name
                    st.success(f"Document processed: {uploaded_file.name}")

                    # Clear previous chat and add a welcome message
                    if "messages" in st.session_state:
                        st.session_state.messages = []
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": f"I've processed {uploaded_file.name}. What would you like to know about it?",
                            }
                        )
                        st.rerun()
                else:
                    st.error(
                        "Could not extract text from the PDF. Please try another document."
                    )

    # Display chat interface
    display_chat_container(st.session_state.llm_interface.process_query)
