# rag_pdf_streamlit/app/pages/page_2.py
import streamlit as st


def about_page():
    st.title("About this Application")

    st.markdown("""
    ## PDF Chat Assistant

    This application allows you to upload PDF documents and have a conversation about their contents.
    The app uses a Retrieval-Augmented Generation (RAG) system to:

    1. Process your uploaded PDF
    2. Extract and index the text content
    3. Retrieve relevant information based on your questions
    4. Generate accurate answers using the context from your document

    ### How to use

    1. Go to the "Chat with PDF" page
    2. Upload your PDF document using the sidebar
    3. Wait for the document to be processed
    4. Ask questions about the content of your document

    ### Technologies Used

    - Streamlit for the web interface
    - LangChain for the RAG pipeline
    - OpenAI's models for embeddings and chat responses
    - FAISS for vector storage and similarity search

    ### Privacy

    Your documents are processed temporarily and are not stored permanently on any servers.
    """)

    st.subheader("Contact")
    st.markdown("For questions or support, please contact us at example@example.com")
