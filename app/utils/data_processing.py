# rag_pdf_streamlit/app/utils/data_processing.py
import os
import tempfile
import streamlit as st
from typing import List, Dict, Optional
import PyPDF2
from io import BytesIO


def extract_text_from_pdf(pdf_file) -> List[str]:
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text_content = []

    # Extract text from each page
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text.strip():  # Only add if there's actual text content
            text_content.append(text)

    return text_content


def process_uploaded_file(uploaded_file) -> Optional[List[str]]:
    """Process an uploaded file and extract text"""
    if uploaded_file is None:
        return None

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Extract text from the temporary file
        with open(temp_file_path, "rb") as file:
            text_content = extract_text_from_pdf(file)

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return text_content

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None
