import streamlit as st
import os
from video_module import YouTubeProcessor
from webscrape_module import WebsiteProcess
from docs_module import DocumentProcessor
import tempfile

# Page config
st.set_page_config(
    page_title="AI Researcher & Educational",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize processors in session state
@st.cache_resource
def get_processors():
    return {
        'youtube': YouTubeProcessor(),
        'website': WebsiteProcess(),
        'document': DocumentProcessor()
    }

processors = get_processors()

# Initialize session state for chat histories
if 'video_chat_history' not in st.session_state:
    st.session_state.video_chat_history = []
if 'website_chat_history' not in st.session_state:
    st.session_state.website_chat_history = []
if 'document_chat_history' not in st.session_state:
    st.session_state.document_chat_history = []

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2e86de;
        margin-bottom: 2rem;
    }
    .tab-header {
        color: #54a0ff;
        border-bottom: 2px solid #54a0ff;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🤖 Multimodal AI Researcher & Educational</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎥 Process Video", 
    "💬 Chat with Video", 
    "🌐 Process Website", 
    "🗨️ Chat with Website", 
    "📄 Process Document", 
    "📝 Chat with Document"
])

# Tab 1: Process Video
with tab1:
    st.markdown('<h3 class="tab-header">Process YouTube Video</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_input = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="video_url"
        )
        process_video_btn = st.button("🎬 Process Video", type="primary", key="process_video")
    
    with col2:
        status_container = st.container()
    
    if process_video_btn and url_input:
        with status_container:
            with st.spinner("Processing video..."):
                try:
                    result = processors['youtube'].process_video(url_input)
                    st.success("✅ Video processed successfully!")
                    
                    # Store results in session state
                    st.session_state.video_transcript = result['transcript']
                    st.session_state.video_summary = result['summary']
                    
                except Exception as e:
                    st.error(f"❌ Error processing video: {str(e)}")
    
    # Display results if available
    if hasattr(st.session_state, 'video_transcript') and hasattr(st.session_state, 'video_summary'):
        col3, col4 = st.columns(2)
        
        with col3:
            st.text_area(
                "Full Transcript",
                value=st.session_state.video_transcript,
                height=300,
                key="transcript_display"
            )
        
        with col4:
            st.text_area(
                "Summary",
                value=st.session_state.video_summary,
                height=300,
                key="summary_display"
            )

# Tab 2: Chat with Video
with tab2:
    st.markdown('<h3 class="tab-header">💬 Have a conversation with the video content</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.video_chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        video_question = st.text_input(
            "Ask a question about the video",
            placeholder="What is this video about?",
            key="video_chat_input"
        )
        
        col_send, col_clear = st.columns([1, 4])
        with col_send:
            send_video_btn = st.button("📤 Send", type="primary", key="send_video")
    
    with col2:
        reset_video_btn = st.button("🔄 Reset Conversation", key="reset_video")
        if reset_video_btn:
            st.session_state.video_chat_history = []
            processors['youtube'].reset_conversation()
            st.success("✅ Conversation reset!")
    
    if send_video_btn and video_question:
        if hasattr(processors['youtube'], 'conversation_chain') and processors['youtube'].conversation_chain:
            with st.spinner("Thinking..."):
                response = processors['youtube'].chat_with_video(video_question)
                st.session_state.video_chat_history.append({'role': 'user', 'content': video_question})
                st.session_state.video_chat_history.append({'role': 'assistant', 'content': response})
                st.rerun()
        else:
            st.error("❌ Please process a video first!")

# Tab 3: Process Website
with tab3:
    st.markdown('<h3 class="tab-header">Process Website</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url_web_input = st.text_input(
            "Website URL",
            placeholder="https://website.com/...",
            key="website_url"
        )
        process_web_btn = st.button("🌐 Process Website", type="primary", key="process_website")
    
    with col2:
        web_status_container = st.container()
    
    if process_web_btn and url_web_input:
        with web_status_container:
            with st.spinner("Processing website..."):
                try:
                    text, summary, status = processors['website'].process_website(url_web_input)
                    if "successfully" in status:
                        st.success("✅ Website processed successfully!")
                        st.session_state.website_text = text
                        st.session_state.website_summary = summary
                    else:
                        st.error(f"❌ {status}")
                except Exception as e:
                    st.error(f"❌ Error processing website: {str(e)}")
    
    # Display results if available
    if hasattr(st.session_state, 'website_text') and hasattr(st.session_state, 'website_summary'):
        col3, col4 = st.columns(2)
        
        with col3:
            st.text_area(
                "Website Content",
                value=st.session_state.website_text,
                height=300,
                key="website_content_display"
            )
        
        with col4:
            st.text_area(
                "Summary",
                value=st.session_state.website_summary,
                height=300,
                key="website_summary_display"
            )

# Tab 4: Chat with Website
with tab4:
    st.markdown('<h3 class="tab-header">🗨️ Have a conversation with the website content</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.website_chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        website_question = st.text_input(
            "Ask a question about the website",
            placeholder="What is this website about?",
            key="website_chat_input"
        )
        
        col_send, col_clear = st.columns([1, 4])
        with col_send:
            send_web_btn = st.button("📤 Send", type="primary", key="send_website")
    
    with col2:
        reset_web_btn = st.button("🔄 Reset Conversation", key="reset_website")
        if reset_web_btn:
            st.session_state.website_chat_history = []
            processors['website'].reset_website_conversation()
            st.success("✅ Conversation reset!")
    
    if send_web_btn and website_question:
        if hasattr(processors['website'], 'conversation_chain') and processors['website'].conversation_chain:
            with st.spinner("Thinking..."):
                response = processors['website'].chat_with_website_content(website_question)
                st.session_state.website_chat_history.append({'role': 'user', 'content': website_question})
                st.session_state.website_chat_history.append({'role': 'assistant', 'content': response})
                st.rerun()
        else:
            st.error("❌ Please process a website first!")

# Tab 5: Process Document
with tab5:
    st.markdown('<h3 class="tab-header">📄 Process PDF, DOCX, or TXT documents</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=['pdf', 'docx', 'txt'],
            key="document_upload"
        )
        process_doc_btn = st.button("📄 Process Document", type="primary", key="process_document")
    
    with col2:
        doc_status_container = st.container()
    
    if process_doc_btn and uploaded_file:
        with doc_status_container:
            with st.spinner("Processing document..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    text, summary, status = processors['document'].process_document(tmp_file_path)
                    
                    # Clean up temp file
                    os.unlink(tmp_file_path)
                    
                    if "successfully" in status:
                        st.success("✅ Document processed successfully!")
                        st.session_state.document_text = text
                        st.session_state.document_summary = summary
                    else:
                        st.error(f"❌ {status}")
                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")
    
    # Display results if available
    if hasattr(st.session_state, 'document_text') and hasattr(st.session_state, 'document_summary'):
        col3, col4 = st.columns(2)
        
        with col3:
            st.text_area(
                "Document Text",
                value=st.session_state.document_text,
                height=300,
                key="document_text_display"
            )
        
        with col4:
            st.text_area(
                "Document Summary",
                value=st.session_state.document_summary,
                height=300,
                key="document_summary_display"
            )

# Tab 6: Chat with Document
with tab6:
    st.markdown('<h3 class="tab-header">📝 Have a conversation with the document content</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Display chat history
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.document_chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**AI:** {message['content']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        document_question = st.text_input(
            "Ask a question about the document",
            placeholder="What is this document about?",
            key="document_chat_input"
        )
        
        col_send, col_clear = st.columns([1, 4])
        with col_send:
            send_doc_btn = st.button("📤 Send", type="primary", key="send_document")
    
    with col2:
        reset_doc_btn = st.button("🔄 Reset Conversation", key="reset_document")
        if reset_doc_btn:
            st.session_state.document_chat_history = []
            processors['document'].reset_document_conversation()
            st.success("✅ Conversation reset!")
    
    if send_doc_btn and document_question:
        if hasattr(processors['document'], 'document_conversation_chain') and processors['document'].document_conversation_chain:
            with st.spinner("Thinking..."):
                response = processors['document'].chat_with_document(document_question)
                st.session_state.document_chat_history.append({'role': 'user', 'content': document_question})
                st.session_state.document_chat_history.append({'role': 'assistant', 'content': response})
                st.rerun()
        else:
            st.error("❌ Please process a document first!")

# Sidebar with information
with st.sidebar:
    st.markdown("## 🤖 AI Researcher & Educational")
    st.markdown("---")
    st.markdown("Created by [Ahmed Yusri](https://www.linkedin.com/in/ahmed-yusri)")
    st.markdown("### Features:")
    st.markdown("• 🎥 YouTube video processing")
    st.markdown("• 🌐 Website content analysis")
    st.markdown("• 📄 Document processing (PDF, DOCX, TXT)")
    st.markdown("• 💬 AI-powered chat with all content types")
    st.markdown("• 🌍 Multi-language support")
    st.markdown("---")
    st.markdown("### Instructions:")
    st.markdown("1. **Process** your content first")
    st.markdown("2. **Chat** with the processed content")
    st.markdown("3. **Reset** conversations when needed")
    st.markdown("---")
    st.markdown("*Powered by OpenAI & LangChain*")

if __name__ == "__main__":
    st.write("Ready to process and chat with your content! 🚀")