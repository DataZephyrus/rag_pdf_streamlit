import streamlit as st


def display_chat_history(messages):
    """Displays the chat history."""
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def chat_input_area(llm, messages):
    """Handles user input and LLM response."""
    if prompt := st.chat_input("Ask a question about your document"):
        messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                response = llm.process_query(prompt)
                message_placeholder.markdown(response)
                messages.append({"role": "assistant", "content": response})
            except Exception as e:
                message_placeholder.markdown(f"Error: {e}")


def display_chat_container(llm):
    """Displays the main chat interface."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    display_chat_history(st.session_state.messages)
    chat_input_area(llm, st.session_state.messages)


def clear_chat_history():
    """Clears the chat history."""
    if "messages" in st.session_state:
        del st.session_state.messages
    st.rerun()
