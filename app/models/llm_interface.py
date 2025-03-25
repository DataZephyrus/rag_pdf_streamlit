import os
from typing import Dict, List, Optional

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from app.utils.openlayer_integration import get_openlayer_handler, trace_function


class LLMInterface:
    def __init__(
        self,
        openai_api_key: str,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
    ):
        """Initializes the LLM interface."""
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.embeddings = OpenAIEmbeddings()

        # Get Openlayer handler if configured
        self.callbacks = []
        openlayer_handler = get_openlayer_handler()
        if openlayer_handler:
            self.callbacks.append(openlayer_handler)

        self.llm = ChatOpenAI(
            model_name=model_name, temperature=temperature, callbacks=self.callbacks
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.chain = None
        self.vector_store = None

    @trace_function
    def initialize_retrieval_chain(self, documents: List[str]) -> bool:
        """Initializes the retrieval chain."""
        if not documents:
            return False
        try:
            self.vector_store = FAISS.from_texts(documents, self.embeddings)
            template = """Use the following pieces of context to answer the question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            {context}

            Question: {question}
            """
            qa_prompt = PromptTemplate(
                template=template, input_variables=["context", "question"]
            )
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(),
                memory=self.memory,
                combine_docs_chain_kwargs={"prompt": qa_prompt},
                callbacks=self.callbacks,
            )
            return True
        except Exception as e:
            st.error(f"Error initializing LLM: {e}")
            return False

    @trace_function
    def process_query(self, query: str) -> str:
        """Processes a query using the retrieval chain."""
        if not self.chain:
            return "Please upload a document first."
        try:
            result = self.chain({"question": query})
            return result["answer"]
        except Exception as e:
            return f"Error processing your question: {e}"

    def reset(self):
        """Resets the chain and memory."""
        self.chain = None
        self.vector_store = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
