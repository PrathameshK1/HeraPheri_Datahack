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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
from vega_datasets import data
import geopandas as gpd

# Function to display the PDF of a given file
def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# Visualization functions
def generate_dummy_data():
    np.random.seed(42)
    return pd.DataFrame({
        'Category': np.random.choice(['Network', 'Application', 'Data', 'Physical'], 100),
        'Risk_Score': np.random.randint(1, 101, 100),
        'Impact_Score': np.random.randint(1, 101, 100),
        'Vulnerability_Type': np.random.choice(['SQL Injection', 'XSS', 'CSRF', 'Buffer Overflow', 'Misconfiguration'], 100),
        'Detection_Time': np.random.randint(1, 1001, 100),
        'Resolution_Time': np.random.randint(1, 2001, 100),
        'Date': pd.date_range(start='2023-01-01', periods=100),
    })

def create_risk_impact_chart(data):
    fig = px.scatter(data, x='Risk_Score', y='Impact_Score', color='Category',
                     size='Risk_Score', hover_data=['Vulnerability_Type'],
                     labels={'Risk_Score': 'Risk Score', 'Impact_Score': 'Impact Score'},
                     title='Risk vs Impact Analysis')
    fig.update_layout(height=500)
    return fig

def create_vulnerability_distribution(data):
    vuln_count = data['Vulnerability_Type'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=vuln_count.index, values=vuln_count.values, hole=.3)])
    fig.update_layout(title_text='Vulnerability Distribution', height=500)
    return fig

def create_detection_resolution_chart(data):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Detection Time', 'Resolution Time'))
    fig.add_trace(go.Box(y=data['Detection_Time'], name='Detection Time'), row=1, col=1)
    fig.add_trace(go.Box(y=data['Resolution_Time'], name='Resolution Time'), row=1, col=2)
    fig.update_layout(height=500, title_text="Detection and Resolution Time Analysis")
    return fig

def create_trend_chart(data):
    daily_risks = data.groupby('Date')['Risk_Score'].mean().reset_index()
    chart = alt.Chart(daily_risks).mark_line().encode(
        x='Date:T',
        y='Risk_Score:Q',
        tooltip=['Date', 'Risk_Score']
    ).properties(
        width=700,
        height=300,
        title='Risk Score Trend Over Time'
    ).interactive()
    return chart

def create_heatmap(data):
    heatmap_data = data.pivot_table(index='Category', columns='Vulnerability_Type', values='Risk_Score', aggfunc='mean')
    fig = px.imshow(heatmap_data, labels=dict(color="Risk Score"),
                    title="Risk Heatmap: Category vs Vulnerability Type")
    fig.update_layout(height=500)
    return fig

def create_3d_risk_bubble(data):
    fig = px.scatter_3d(
        data, 
        x='Risk_Score', 
        y='Impact_Score', 
        z='Resolution_Time', 
        color='Category',
        size='Risk_Score',
        hover_data=['Vulnerability_Type'],
        title='3D Risk Analysis: Risk vs Impact vs Resolution Time',
        labels={'Risk_Score': 'Risk Score', 'Impact_Score': 'Impact Score', 'Resolution_Time': 'Resolution Time'}
    )
    fig.update_layout(height=700)
    return fig



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
    st.title("📊 Advanced Cybersecurity Dashboard")
    st.markdown("---")

    # Generate dummy data
    data = generate_dummy_data()

    # Sidebar for filtering
    st.sidebar.header("Filters")
    selected_categories = st.sidebar.multiselect("Select Categories", data['Category'].unique(), default=data['Category'].unique())
    date_range = st.sidebar.date_input("Select Date Range", [data['Date'].min(), data['Date'].max()])

    # Apply filters
    filtered_data = data[
        (data['Category'].isin(selected_categories)) &
        (data['Date'] >= pd.Timestamp(date_range[0])) &
        (data['Date'] <= pd.Timestamp(date_range[1]))
    ]

    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Risk Score", f"{filtered_data['Risk_Score'].mean():.2f}")
    col2.metric("Average Impact Score", f"{filtered_data['Impact_Score'].mean():.2f}")
    col3.metric("Total Vulnerabilities", len(filtered_data))
    col4.metric("Avg. Resolution Time (hrs)", f"{filtered_data['Resolution_Time'].mean() / 60:.2f}")

    # Risk vs Impact Interactive Scatter Plot
    st.plotly_chart(create_risk_impact_chart(filtered_data), use_container_width=True)

    # Vulnerability Distribution Pie Chart
    st.plotly_chart(create_vulnerability_distribution(filtered_data), use_container_width=True)

    # Detection and Resolution Time Box Plots
    st.plotly_chart(create_detection_resolution_chart(filtered_data), use_container_width=True)

    # Risk Score Trend Chart
    st.altair_chart(create_trend_chart(filtered_data), use_container_width=True)

    # Risk Heatmap
    st.plotly_chart(create_heatmap(filtered_data), use_container_width=True)

    # Use the function to create the 3D plot
    st.plotly_chart(create_3d_risk_bubble(filtered_data), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© 2024 Cybersecurity Assessment Bot. All rights reserved. 🛡️")

