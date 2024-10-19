# 🛡️ Kavach: Cybersecurity Assessment Bot

![Kavach](logo.png)

**Kavach** is a powerful Streamlit-based application designed to simplify cybersecurity assessments. Upload your infrastructure documentation, conduct comprehensive security evaluations, and receive actionable recommendations through an intelligent chatbot interface. 🚀

## 🛠️ Features

- **📊 Cybersecurity Assessment**: Conduct thorough evaluations of your organization's security posture.
- **📄 Documentation Analysis**: Upload and analyze infrastructure documentation for potential vulnerabilities.
- **🤖 AI-Powered Chatbot**: Interact with an intelligent assistant to get insights and recommendations.
- **📝 Detailed Reporting**: Generate comprehensive reports with risk assessments and actionable steps.
- **🌟 User-Friendly Interface**: Enjoy a sleek and intuitive UI with emojis and responsive design for enhanced user experience.

## 🖥️ Tech Stack

Kavach leverages a combination of cutting-edge technologies to deliver a seamless and efficient user experience. Here's a breakdown of the technologies and tools used:

- **[LangChain](https://langchain.readthedocs.io/)**: Utilized as the orchestration framework to manage the flow between different components, including embeddings creation, vector storage, and chatbot interactions.
  
- **[Unstructured](https://github.com/Unstructured-IO/unstructured)**: Employed for robust document processing, enabling the extraction and preprocessing of text from uploaded documentation.
  
- **[BGE Embeddings from HuggingFace](https://huggingface.co/BAAI/bge-small-en)**: Used to generate high-quality embeddings for the processed documents, facilitating effective semantic search and retrieval.
  
- **[Qdrant](https://qdrant.tech/)**: A vector database running locally via Docker, responsible for storing and managing the generated embeddings for fast and scalable retrieval.
  
- **[LLaMA 3.2 via Ollama](https://ollama.com/)**: Integrated as the local language model to power the chatbot, providing intelligent and context-aware responses based on the document embeddings.
  
- **[Streamlit](https://streamlit.io/)**: The core framework for building the interactive web application, offering an intuitive interface for users to conduct assessments, analyze documentation, and interact with the chatbot.

## 📁 Directory Structure

kavach/
