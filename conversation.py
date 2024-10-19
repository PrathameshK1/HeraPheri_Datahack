import streamlit as st
import requests

API_URL = "http://localhost:3000/api/v1/prediction/eeea81ea-1c4f-4bff-a36e-0b19bccc7881"

def query(payload):
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None

def main():
    st.title("AI Chat Interface 💬")

    user_question = st.text_input("Enter your message:")

    if st.button("Send"):
        if user_question.strip() != "":
            payload = {"question": user_question}
            
            with st.spinner("Waiting for response..."):
                output = query(payload)

            if output:
                response_text = output.get("text", "No response text available")
                
                st.success("API Response:")
                st.write(response_text)
        else:
            st.warning("Please enter a message to send.")

if __name__ == "__main__":
    main()