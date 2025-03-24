# rag_pdf_streamlit/app/models/llm_interface.py
import os
from typing import Dict, List, Optional

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS


class LLMInterface:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.2,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.chain = None
        self.vector_store = None

    def initialize_retrieval_chain(self, documents: List[str]):
        """Initialize the retrieval chain with documents"""
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        texts = text_splitter.create_documents(documents)

        # Create vector store
        self.vector_store = FAISS.from_documents(texts, self.embeddings)

        # Create prompt template
        template = """You are a helpful AI assistant that answers questions based on the provided documents.
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        """
        QA_PROMPT = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        # Create retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        )

        return True

    def process_query(self, query: str) -> str:
        """Process a query using the retrieval chain"""
        if not self.chain:
            return "Please upload a document first."

        try:
            response = self.chain({"question": query})
            return response["answer"]
        except Exception as e:
            return f"Error processing your question: {str(e)}"

    def reset(self):
        """Reset the chain and memory"""
        self.chain = None
        self.vector_store = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
