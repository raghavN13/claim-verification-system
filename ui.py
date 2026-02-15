import streamlit as st
from verifier import verify_claim
from vector_db import count_documents

st.set_page_config(
    page_title="Claim Verification Assistant",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Real-Time Claim Verification Assistant")

st.write("Verify news claims using AI + RAG + Live Web Evidence")

# Show knowledge base size
kb_size = count_documents()
# st.info(f"Knowledge Base Size: {kb_size} documents")

# Input box
claim = st.text_area(
    "Enter claim to verify:",
    height=100,
    placeholder="Example: India became the 4th largest economy"
)

# Verify button
if st.button("Verify Claim"):

    if not claim.strip():
        st.warning("Please enter a claim.")
    else:
        with st.spinner("Verifying claim..."):

            result = verify_claim(claim)

        st.success("Verification Complete")

        st.subheader("Result:")

        st.write(result)