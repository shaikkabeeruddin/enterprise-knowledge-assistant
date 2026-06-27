"""
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Enterprise Knowledge Assistant")
st.write("Upload a PDF and ask questions about its contents.")

# -------------------
# Upload Section
# -------------------
st.subheader("Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    if st.button("Process PDF"):
        with st.spinner("Processing PDF and creating embeddings..."):
            try:
                response = requests.post(
                    f"{API_URL}/upload/",
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("PDF processed successfully!")
                    st.write(f"**File:** {result.get('filename', uploaded_file.name)}")
                    st.write(f"**New Chunks:** {result.get('num_new_chunks', 'N/A')}")
                    st.write(f"**Total Chunks in Index:** {result.get('num_total_chunks', 'N/A')}")
                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Upload failed: {e}")

# -------------------
# Ask Questions Section
# -------------------
st.divider()
st.subheader("Ask Questions")

question = st.text_input("Ask a question about the uploaded PDF")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "question": question
        }

        try:
            with st.spinner("Generating answer..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload
                )

            if response.status_code == 200:
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.subheader("Answer")
                    st.write(result.get("answer", "No answer returned."))

                    sources = result.get("sources", [])
                    if sources:
                        st.subheader("Sources")
                        for i, source in enumerate(sources, 1):
                            doc = source.get("document", "Unknown document")
                            page = source.get("page", "N/A")
                            st.write(f"{i}. **{doc}** — Page {page}")

                    confidence = result.get("confidence")
                    if confidence is not None:
                        st.caption(f"Confidence: {confidence}")

            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Request failed: {e}")"""
            
            
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Enterprise Knowledge Assistant")
st.write("Upload a PDF and ask questions about its contents.")

# -------------------
# Upload Section
# -------------------
st.subheader("Upload Document")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    if st.button("Process PDF"):
        with st.spinner("Processing PDF and creating embeddings..."):
            try:
                response = requests.post(
                    f"{API_URL}/upload/",
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success("PDF processed successfully!")
                    st.write(f"**File:** {result.get('filename', uploaded_file.name)}")
                    st.write(f"**New Chunks:** {result.get('num_new_chunks', 'N/A')}")
                    st.write(f"**Total Chunks in Index:** {result.get('num_total_chunks', 'N/A')}")
                else:
                    st.error(response.text)

            except Exception as e:
                st.error(f"Upload failed: {e}")

# -------------------
# Ask Questions Section
# -------------------
st.divider()
st.subheader("Ask Questions")

question = st.text_input("Ask a question about the uploaded PDF")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "question": question
        }

        try:
            with st.spinner("Generating answer..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json=payload
                )

            if response.status_code == 200:
                result = response.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])
                    confidence = result.get("confidence")

                    st.subheader("Answer")
                    st.write(answer)

                    normalized_answer = answer.strip().lower()

                    # Show sources only if answer is not "I don't know..."
                    if normalized_answer != "i don't know based on the available documents." and sources:
                        st.subheader("Sources")
                        for i, source in enumerate(sources, 1):
                            doc = source.get("document", "Unknown document")
                            page = source.get("page")

                            if page is None:
                                st.write(f"{i}. **{doc}**")
                            else:
                                st.write(f"{i}. **{doc}** — Page {page}")

                    if confidence is not None:
                        st.caption(f"Confidence: {confidence}")

            else:
                st.error(response.text)

        except Exception as e:
            st.error(f"Request failed: {e}")