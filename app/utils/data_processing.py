import os
import tempfile
import streamlit as st
from typing import List, Optional
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.utils.openlayer_integration import trace_function


@trace_function
def extract_text_from_pdf(pdf_file) -> Optional[List[str]]:
    """Extracts text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = [
            page.extract_text()
            for page in pdf_reader.pages
            if page.extract_text().strip()
        ]
        return text_content
    except PyPDF2.errors.PdfReadError as e:
        st.error(f"Error reading PDF: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading the PDF: {e}")
        return None


@trace_function
def process_uploaded_file(uploaded_file) -> Optional[List[str]]:
    """Processes an uploaded file and extracts text."""
    if uploaded_file is None:
        return None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name
        with open(temp_file_path, "rb") as file:
            text_content = extract_text_from_pdf(file)
            if text_content:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200
                )
                # Create proper Document objects instead of dictionaries
                docs = [Document(page_content=content) for content in text_content]
                texts = text_splitter.split_documents(docs)
                return [doc.page_content for doc in texts]
            else:
                return None
        os.unlink(temp_file_path)
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return None
