# rag_pdf_streamlit/app/components/chatbot_ui.py
from typing import Callable, Dict, List

import streamlit as st


def initialize_chat_ui():
    """Initialize the chat history in the session state if it doesn't exist"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = True
        st.session_state.messages.append({"role": "assistant", "content": "Hello! I'm ready to help you with your PDFs. Please upload a document to get started."})

def display_chat_history():
    """Display all messages in the chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def chat_input_area(process_query_func: Callable):
    """Create the chat input area and handle new messages"""
    if prompt := st.chat_input("Ask a question about your document"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display the new user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Process the query and get the response
            response = process_query_func(prompt)
            
            # Update the placeholder with the full response
            message_placeholder.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def display_chat_container(process_query_func: Callable):
    """Main function to display the entire chat interface"""
    initialize_chat_ui()
    display_chat_history()
    chat_input_area(process_query_func)

def clear_chat_history():
    """Function to clear the chat history"""
    if "messages" in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_initialized = False
    st.rerun()