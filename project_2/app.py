import streamlit as st
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_ollama import ChatOllama

# Set page config
st.set_page_config(
    page_title="Everstorm Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

@st.cache_resource
def load_documents():
    """Load and process PDF documents"""
    pdf_paths = glob.glob("data/Everstorm_*.pdf")
    raw_docs = []

    for pdf_path in pdf_paths:
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            raw_docs.extend(pages)
        except Exception as e:
            st.warning(f"Error loading {pdf_path}: {e}")
            continue

    if not raw_docs:
        st.error("No documents found! Please ensure PDF files are in the 'data/' directory.")
        return None, None, None

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = text_splitter.split_documents(raw_docs)

    # Create embeddings
    embedder = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Build vector store
    vectordb = FAISS.from_documents(chunks, embedder)
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})

    return retriever, embedder, chunks

@st.cache_resource
def load_llm():
    """Load the Ollama LLM"""
    try:
        llm = ChatOllama(model="gemma3:1b", temperature=0.1)
        return llm
    except Exception as e:
        st.error(f"Error loading LLM: {e}")
        return None

def main():
    st.title("🤖 Everstorm Customer Support Chatbot")
    st.markdown("Ask questions about Everstorm's policies and services!")

    # Load components
    retriever, embedder, chunks = load_documents()
    llm = load_llm()

    if retriever is None or llm is None:
        st.stop()

    # Simple template for responses
    simple_template = """
    You are a Customer Support Chatbot. Use only the information in CONTEXT to answer.
    If the answer is not in CONTEXT, respond with "I'm not sure from the docs."

    CONTEXT:
    {context}

    USER:
    {question}
    """

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

        # Get relevant documents
        docs = retriever.invoke(prompt)
        context = "\n\n".join([doc.page_content for doc in docs])

        # Create the prompt with simple template
        formatted_prompt = simple_template.format(context=context, question=prompt)

        # Get response from LLM
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = llm.invoke(formatted_prompt)
                    answer = response.content

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

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

        st.header("📊 Statistics")
        st.write(f"📄 Documents loaded: {len(chunks)} chunks")
        st.write(f"🔍 Vector store ready: ✅")
        st.write(f"🤖 LLM model: gemma3:1b")

if __name__ == "__main__":
    main()
