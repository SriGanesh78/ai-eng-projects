import streamlit as st
import os
import glob
import json
import time

# Set page config
st.set_page_config(
    page_title="Everstorm Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

def simulate_rag_response(question):
    """Simulate RAG response based on question keywords"""

    # Mock responses based on question content
    responses = {
        "return": "Based on Everstorm's return policy, you have 30 days from purchase to return items. Items must be in original condition with tags attached. To start a return, contact our customer service team.",
        "refund": "Everstorm offers full refunds for eligible returns within 30 days. Refunds are processed within 5-7 business days after we receive your returned item.",
        "shipping": "Standard shipping takes 3-5 business days within the continental US. You can track your package using the tracking number provided in your shipping confirmation email.",
        "delivery": "Delivery times vary by location. Standard delivery is 3-5 business days, express delivery is 1-2 business days. You'll receive tracking information via email.",
        "exchange": "We offer exchanges for items in original condition within 30 days. Size exchanges are free, but you'll need to pay return shipping for other exchanges.",
        "payment": "Everstorm accepts all major credit cards, PayPal, and Apple Pay. All transactions are secure and encrypted for your protection.",
        "security": "Your payment information is protected with industry-standard encryption. We never store your complete credit card details on our servers.",
        "sizing": "Please refer to our detailed sizing chart in the product description. If you're between sizes, we recommend sizing up for the best fit.",
        "care": "Most Everstorm items are machine washable on gentle cycle. Please check the care label on each item for specific instructions.",
        "contact": "You can reach our customer support team at support@everstorm.com or call 1-800-EVERSTORM. We're available Monday-Friday 9AM-6PM EST.",
        "support": "Our customer support team is here to help! Contact us via email, phone, or live chat for assistance with orders, returns, or any questions."
    }

    # Find relevant response based on keywords
    question_lower = question.lower()
    for keyword, response in responses.items():
        if keyword in question_lower:
            return response

    # Default response if no keywords match
    return "Thank you for your question! Our customer support team can help you with that. Please contact us at support@everstorm.com or call 1-800-EVERSTORM for personalized assistance."

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
        st.info("Please ensure PDF files are in the 'data/' directory.")

    # Sidebar with sample questions
    st.sidebar.header("💡 Sample Questions")

    sample_questions = [
        "What is your return policy?",
        "How long does shipping take?",
        "How can I contact customer support?",
        "What payment methods do you accept?",
        "How do I exchange an item?",
        "What is your refund policy?",
        "How do I track my order?",
        "What are your sizing guidelines?",
        "How should I care for my items?",
        "Is my payment information secure?"
    ]

    for question in sample_questions:
        if st.sidebar.button(question, key=f"sample_{question}"):
            st.session_state.user_input = question

    # Chat interface
    st.header("💬 Chat with the Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about Everstorm's policies..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Simulate processing time
                time.sleep(1)
                response = simulate_rag_response(prompt)
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Handle sample question selection
    if hasattr(st.session_state, 'user_input'):
        prompt = st.session_state.user_input
        delattr(st.session_state, 'user_input')

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)
                response = simulate_rag_response(prompt)
                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Footer
    st.markdown("---")
    st.markdown("**Note**: This is a demo version. In production, this would connect to a full RAG pipeline with document retrieval and LLM generation.")

    # System status
    st.sidebar.header("📊 System Status")
    st.sidebar.success("✅ App Running")
    st.sidebar.info(f"📄 {len(pdf_files)} Documents Ready")
    st.sidebar.info("🤖 Mock RAG Active")
    st.sidebar.info("💬 Chat Interface Ready")

if __name__ == "__main__":
    main()
