import streamlit as st
from transformers import pipeline

#  pipeline model Integration
#  use st.cache_resource so the AI model doesn't reload every time you type
@st.cache_resource 
def load_qa_model():
    # Tech Stack: HuggingFace Transformers
    # This model is small, fast, and great for extractive Q&A
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Initialize the model
qa_pipeline = load_qa_model()

# --- UI Setup ---
st.set_page_config(page_title="NLP Q&A System", page_icon="🧠")
st.title("🤖 AI Intern: Smart Q&A Explorer")
st.markdown("Build a question-answering app using HuggingFace pre-trained models.")
st.divider()

#  Input context + question
st.subheader("Step 1: Provide Knowledge Base")
context = st.text_area(
    "Paste your text/article here:", 
    height=200, 
    placeholder="Example: The Great Wall of China is a series of fortifications that were built across the historical northern borders of ancient Chinese states..."
)

st.subheader("Step 2: Ask a Question")
question = st.text_input("What would you like to find in the text?", placeholder="e.g., Where was the wall built?")

#  output format
if st.button("Extract Answer ✨"):
    if context and question:
        with st.spinner("Searching through the context..."):
            # The actual NLP inference
            result = qa_pipeline(question=question, context=context)
            
            # Displaying the answer beautifully
            st.markdown("---")
            st.markdown("### 🎯 Answer Found:")
            st.success(f"**{result['answer']}**")
            
            # Show confidence score
            confidence = round(result['score'] * 100, 2)
            st.progress(result['score'])
            st.caption(f"Confidence Score: {confidence}%")
    else:
        st.warning("Please fill in both the context and the question fields.")

# Unique Feature: Sidebar Info
st.sidebar.title("Task Details")
st.sidebar.info("""
**Project:** QNA Model  
**Model:** DistilBERT (SQuAD)  
**Task:** Week 2 NLP Intern Task
""")