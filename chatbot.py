# chatbot.py

import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_ollama import ChatOllama
from qdrant_client import QdrantClient
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import streamlit as st
from huggingface_hub import snapshot_download
from transformers import AutoModel, AutoTokenizer
import json
from typing import List, Dict
import PyPDF2
import docx
import re

class ChatbotManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        llm_model: str = "llama3.2:3b",
        llm_temperature: float = 0.7,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "vector_db",
    ):
        """
        Initializes the ChatbotManager with embedding models, LLM, and vector store.

        Args:
            model_name (str): The HuggingFace model name for embeddings.
            device (str): The device to run the model on ('cpu' or 'cuda').
            encode_kwargs (dict): Additional keyword arguments for encoding.
            llm_model (str): The local LLM model name for ChatOllama.
            llm_temperature (float): Temperature setting for the LLM.
            qdrant_url (str): The URL for the Qdrant instance.
            collection_name (str): The name of the Qdrant collection.
        """
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        # Download and load the model
        model_path = snapshot_download(repo_id=self.model_name)
        self.model = AutoModel.from_pretrained(model_path).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Initialize Embeddings
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        # Initialize Local LLM
        self.llm = ChatOllama(
            model=self.llm_model,
            temperature=self.llm_temperature,
            # Add other parameters if needed
        )

        # Define the prompt template
        self.prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}
Previous Responses: {previous_responses}

Only return the helpful answer. Answer must be detailed and well explained.
If necessary, ask follow-up questions to gather more information.
Helpful answer:
"""

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=self.qdrant_url, prefer_grpc=False
        )

        # Initialize the Qdrant vector store
        self.db = Qdrant(
            client=self.client,
            embeddings=self.embeddings,
            collection_name=self.collection_name
        )

        # Initialize the prompt
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=['context', 'question', 'previous_responses']
        )

        # Initialize the retriever
        self.retriever = self.db.as_retriever(search_kwargs={"k": 1})

        # Define chain type kwargs
        self.chain_type_kwargs = {"prompt": self.prompt}

        # Initialize the RetrievalQA chain with return_source_documents=False
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,  # Set to False to return only 'result'
            chain_type_kwargs=self.chain_type_kwargs,
            verbose=False
        )

        # Initialize conversation history
        self.conversation_history = []

        # Initialize compliance standards
        self.compliance_standards = {
            "GDPR": self.load_compliance_standard("gdpr.json"),
            "HIPAA": self.load_compliance_standard("hipaa.json")
        }

    def load_compliance_standard(self, filename: str) -> Dict:
        """Load compliance standard from a JSON file."""
        with open(filename, 'r') as f:
            return json.load(f)

    def get_response(self, query: str) -> str:
        """
        Processes the user's query and returns the chatbot's response.

        Args:
            query (str): The user's input question.

        Returns:
            str: The chatbot's response.
        """
        try:
            previous_responses = "\n".join(self.conversation_history)
            response = self.qa.run({"question": query, "previous_responses": previous_responses})
            self.conversation_history.append(response)

            # Check for follow-up questions
            follow_up = self.generate_follow_up(response)
            if follow_up:
                response += f"\n\nFollow-up question: {follow_up}"

            return response
        except Exception as e:
            st.error(f"⚠️ An error occurred while processing your request: {e}")
            return "⚠️ Sorry, I couldn't process your request at the moment."

    def generate_follow_up(self, response: str) -> str:
        """Generate a follow-up question based on the response."""
        # Implement logic to generate follow-up questions
        # This is a placeholder implementation
        if "MFA" in response and "not implemented" in response.lower():
            return "What other access control mechanisms do you have in place?"
        return ""

    def analyze_document(self, file) -> str:
        """Analyze uploaded document for vulnerabilities and compliance gaps."""
        text = self.extract_text(file)
        analysis = self.llm.generate("Analyze the following text for potential security vulnerabilities and compliance gaps:\n\n" + text)
        return analysis

    def extract_text(self, file) -> str:
        """Extract text from various file formats."""
        if file.name.endswith('.pdf'):
            return self.extract_from_pdf(file)
        elif file.name.endswith('.docx'):
            return self.extract_from_docx(file)
        elif file.name.endswith('.txt'):
            return file.read().decode('utf-8')
        else:
            raise ValueError("Unsupported file format")

    def extract_from_pdf(self, file) -> str:
        """Extract text from PDF file."""
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_from_docx(self, file) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    def generate_report(self) -> str:
        """Generate a comprehensive security assessment report."""
        report = "Security Assessment Report\n\n"
        
        # Analyze conversation history
        for response in self.conversation_history:
            vulnerabilities = self.identify_vulnerabilities(response)
            report += f"Identified Vulnerabilities:\n{vulnerabilities}\n\n"
            
            recommendations = self.generate_recommendations(vulnerabilities)
            report += f"Recommendations:\n{recommendations}\n\n"
        
        # Check compliance
        compliance_issues = self.check_compliance()
        report += f"Compliance Issues:\n{compliance_issues}\n\n"
        
        return report

    def identify_vulnerabilities(self, response: str) -> List[str]:
        """Identify vulnerabilities from the response."""
        # Implement logic to identify vulnerabilities
        # This is a placeholder implementation
        vulnerabilities = []
        if "MFA not implemented" in response:
            vulnerabilities.append("Lack of Multi-Factor Authentication")
        return vulnerabilities

    def generate_recommendations(self, vulnerabilities: List[str]) -> List[str]:
        """Generate recommendations based on identified vulnerabilities."""
        # Implement logic to generate recommendations
        # This is a placeholder implementation
        recommendations = []
        if "Lack of Multi-Factor Authentication" in vulnerabilities:
            recommendations.append("Implement Multi-Factor Authentication for all user accounts")
        return recommendations

    def check_compliance(self) -> List[str]:
        """Check compliance against loaded standards."""
        compliance_issues = []
        for standard, requirements in self.compliance_standards.items():
            for requirement in requirements:
                if not self.check_requirement(requirement):
                    compliance_issues.append(f"{standard}: {requirement}")
        return compliance_issues

    def check_requirement(self, requirement: str) -> bool:
        """Check if a specific compliance requirement is met."""
        # Implement logic to check if the requirement is met
        # This is a placeholder implementation
        return any(requirement.lower() in response.lower() for response in self.conversation_history)
