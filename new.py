# app.py

import streamlit as st
from streamlit import session_state
import time
import base64
import os
from vectors import EmbeddingsManager
from chatbot import ChatbotManager
import pandas as pd
from io import StringIO
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Function to display the PDF of a given file
def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Initialize session_state variables
if 'temp_pdf_path' not in st.session_state:
    st.session_state['temp_pdf_path'] = None
if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'uploaded_docs' not in st.session_state:
    st.session_state['uploaded_docs'] = []
if 'assessment_results' not in st.session_state:
    st.session_state['assessment_results'] = {}

# Set page configuration
st.set_page_config(
    page_title="Cybersecurity Assessment Bot",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.markdown("### 🛡️ Cybersecurity Assessment Bot")
    st.markdown("---")
    menu = ["🏠 Home", "📊 Assessment", "📄 Documentation Analysis", "📝 Report", "📈 Visualisation", "📧 Contact"]
    choice = st.selectbox("Navigate", menu)

# Home Page
if choice == "🏠 Home":
    st.title("🛡️ Cybersecurity Assessment Bot")
    st.markdown("""
    Welcome to the **Cybersecurity Assessment Bot**! 🚀

    Our AI-powered bot helps you:
    - Conduct comprehensive cybersecurity assessments
    - Analyze your infrastructure documentation
    - Generate detailed reports with actionable recommendations
    - Verify compliance with industry standards

    Get started by navigating to the Assessment page! 🔒
    """)

# Assessment Page
elif choice == "📊 Assessment":
    st.title("🤖 Cybersecurity Assessment")
    st.markdown("---")

    if st.session_state['chatbot_manager'] is None:
        st.session_state['chatbot_manager'] = ChatbotManager(
            model_name="BAAI/bge-small-en",
            device="cpu",
            encode_kwargs={"normalize_embeddings": True},
            llm_model="llama3.2:3b",
            llm_temperature=0.7,
            qdrant_url="http://localhost:6333",
            collection_name="vector_db"
        )

    # Display existing messages
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).markdown(msg['content'])

    # User input
    if user_input := st.chat_input("Respond to the assessment question..."):
        st.chat_message("user").markdown(user_input)
        st.session_state['messages'].append({"role": "user", "content": user_input})

        with st.spinner("🤖 Analyzing response..."):
            try:
                answer = st.session_state['chatbot_manager'].get_response(user_input)
                time.sleep(1)
            except Exception as e:
                answer = f"⚠️ An error occurred: {e}"
        
        st.chat_message("assistant").markdown(answer)
        st.session_state['messages'].append({"role": "assistant", "content": answer})

        # Update assessment results
        if "vulnerability" in answer.lower() or "risk" in answer.lower():
            st.session_state['assessment_results'][user_input] = "High Risk"
        elif "improvement" in answer.lower():
            st.session_state['assessment_results'][user_input] = "Medium Risk"
        else:
            st.session_state['assessment_results'][user_input] = "Low Risk"

# Documentation Analysis Page
elif choice == "📄 Documentation Analysis":
    st.title("📄 Documentation Analysis")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload infrastructure documentation", type=["pdf", "txt", "json"])
    if uploaded_file is not None:
        st.success(f"📄 {uploaded_file.name} uploaded successfully!")
        st.session_state['uploaded_docs'].append(uploaded_file.name)

        if uploaded_file.type == "application/pdf":
            displayPDF(uploaded_file)
        elif uploaded_file.type == "text/plain":
            content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            st.text_area("File Content", content, height=300)
        elif uploaded_file.type == "application/json":
            content = json.loads(uploaded_file.getvalue())
            st.json(content)

        if st.button("Analyze Document"):
            with st.spinner("🔍 Analyzing document..."):
                # Simulating document analysis
                time.sleep(2)
                st.success("Analysis complete!")
                st.markdown("### Findings:")
                st.markdown("- No mention of encryption protocols")
                st.markdown("- Access control policies need updating")
                st.markdown("- Regular security audits are not scheduled")

# Report Page
elif choice == "📝 Report":
    st.title("📝 Cybersecurity Assessment Report")
    st.markdown("---")

    if st.session_state['assessment_results']:
        st.markdown("### Risk Assessment")
        df = pd.DataFrame.from_dict(st.session_state['assessment_results'], orient='index', columns=['Risk Level'])
        st.dataframe(df)

        st.markdown("### Recommendations")
        st.markdown("1. Implement multi-factor authentication")
        st.markdown("2. Encrypt sensitive data at rest and in transit")
        st.markdown("3. Conduct regular security audits")

        st.markdown("### Analyzed Documents")
        for doc in st.session_state['uploaded_docs']:
            st.markdown(f"- {doc}")

        if st.button("Generate PDF Report"):
            with st.spinner("Generating PDF..."):
                time.sleep(2)
                st.success("PDF Report generated successfully!")
    else:
        st.info("Complete the assessment to generate a report.")

# Contact Page
elif choice == "📧 Contact":
    st.title("📬 Contact Us")
    st.markdown("""
    Need further assistance? Reach out to our cybersecurity experts:

    - **Email:** [security@example.com](mailto:security@example.com) ✉️
    - **Phone:** +1 (555) 123-4567 ☎️

    For urgent security concerns, please contact our 24/7 hotline.
    """)


elif choice == "📈 Visualisation":
    st.title("📈 Visualisation")
    st.markdown("---")
    

    # Generate dummy data
    np.random.seed(42)
    data = pd.DataFrame({
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Value1': np.random.randn(100) * 100,
        'Value2': np.random.randn(100) * 50 + 20,
        'Value3': np.random.randint(1, 100, 100)
    })

    # Bar Chart
    st.markdown("### Bar Chart")
    bar_data = data['Category'].value_counts().reset_index()
    bar_data.columns = ['Category', 'Count']
    st.bar_chart(bar_data.set_index('Category'))

    # Line Chart
    st.markdown("### Line Chart")
    line_data = data[['Value1', 'Value2']].cumsum()
    st.line_chart(line_data)

    # Area Chart
    st.markdown("### Area Chart")
    st.area_chart(line_data)

    # Scatter Plot
    st.markdown("### Scatter Plot")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='Value1', y='Value2', hue='Category', ax=ax)
    st.pyplot(fig)

    # Histogram
    st.markdown("### Histogram")
    fig, ax = plt.subplots()
    sns.histplot(data['Value3'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

    # Box Plot
    st.markdown("### Box Plot")
    fig, ax = plt.subplots()
    sns.boxplot(data=data, x='Category', y='Value1', ax=ax)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("© 2024 Cybersecurity Assessment Bot. All rights reserved. 🛡️")

