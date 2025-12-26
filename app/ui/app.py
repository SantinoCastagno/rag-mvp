import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Gemini RAG Lab", layout="wide")

st.title("Gemini RAG Lab")
st.caption("Powered by Gemini 2.5 Flash-Lite")

# Initialize Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Documents")
    st.caption(f"Session ID: {st.session_state.session_id}")
    uploaded_file = st.file_uploader("Choose a PDF or Markdown file", type=["pdf", "md"])
    
    if uploaded_file is not None:
        if st.button("Ingest File"):
            with st.spinner("Ingesting..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"Error: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# Chat Interface
if "messages" not in st.session_state:
    # Fetch history from backend
    try:
        response = requests.get(f"{API_URL}/history/{st.session_state.session_id}")
        if response.status_code == 200:
            st.session_state.messages = response.json()
        else:
            st.session_state.messages = []
    except Exception as e:
        # If backend is down or new session, start empty
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask something about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat", 
                    json={"question": prompt, "session_id": st.session_state.session_id}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data["sources"]
                    
                    st.markdown(answer)
                    if sources:
                        st.divider()
                        st.caption(f"Sources: {', '.join(sources)}")
                        
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection Error: {e}")