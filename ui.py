import streamlit as st
import requests

# API URL
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG PDF Chatbot")
st.write("Ask questions from your PDF")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
query = st.chat_input("Ask a question...")

if query:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Call API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json={"question": query})

            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]

                # Show answer
                st.markdown(answer)

                # Show sources
                if sources:
                    st.markdown("### 📌 Sources")
                    for src in sources:
                        st.markdown(f"- Page {src['page']} ({src['file']})")

                # Save response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
            else:
                st.error("API Error")