import streamlit as st
import os
import glob

# Set page config
st.set_page_config(
    page_title="Everstorm Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("🤖 Everstorm Customer Support Chatbot")
    st.markdown("Ask questions about Everstorm's policies and services!")

    # Check if PDF files exist
    pdf_files = glob.glob("data/*.pdf")

    if pdf_files:
        st.success(f"✅ Found {len(pdf_files)} PDF documents ready for processing!")

        # Display PDF files
        with st.expander("📄 Available Documents"):
            for pdf_file in pdf_files:
                st.write(f"• {os.path.basename(pdf_file)}")
    else:
        st.error("❌ No PDF files found in the 'data/' directory!")
        st.info("Please ensure your Everstorm PDF files are in the 'data/' folder.")

    # Simple chat interface
    st.subheader("💬 Chat with the Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about Everstorm's services..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Simple response (placeholder for now)
        with st.chat_message("assistant"):
            response = f"I received your question: '{prompt}'. The RAG system is being set up to provide accurate answers from the Everstorm documents."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar with sample questions
    with st.sidebar:
        st.header("💡 Sample Questions")
        sample_questions = [
            "What is your return policy?",
            "How long does shipping take?",
            "How can I contact customer support?",
            "What is your refund policy?",
            "How do I track my order?",
            "What are your operating hours?"
        ]

        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

        st.header("📊 System Status")
        st.write(f"📄 Documents found: {len(pdf_files)}")
        st.write("🔧 RAG system: Setting up...")
        st.write("🤖 LLM model: Preparing...")

        st.header("🔧 Setup Instructions")
        st.info("""
        **Next Steps:**
        1. Ensure all dependencies are properly installed
        2. Fix numpy compatibility issues
        3. Load PDF documents into vector store
        4. Initialize LLM connection
        5. Test the RAG pipeline
        """)

if __name__ == "__main__":
    main()
