# 🤖 Multimodal AI Researcher & Educational Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**An intelligent multi-source content processing platform that transforms YouTube videos, websites, and documents into interactive AI-powered conversations.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies Used](#-technologies-used)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

## 🌟 Overview

The **Multimodal AI Researcher & Educational Platform** is a cutting-edge application that leverages advanced AI technologies to extract, process, and enable interactive conversations with content from multiple sources. Whether you're a researcher, student, or content creator, this platform transforms static content into dynamic, queryable knowledge bases.

### 🎯 Problem Statement

In today's information-rich environment, users struggle to:
- Extract meaningful insights from lengthy video content
- Process and understand complex documents quickly
- Interact with web-based information efficiently
- Maintain context across different content types

### 💡 My Solution

Our platform provides a unified interface that:
- **Processes** diverse content types automatically
- **Generates** intelligent summaries in multiple languages
- **Enables** natural language conversations with any processed content
- **Maintains** conversation context and history

## ✨ Features

### 🎥 YouTube Video Processing
- **Audio Extraction**: High-quality audio extraction using `yt-dlp`
- **Speech-to-Text**: Advanced transcription via OpenAI Whisper API
- **Intelligent Summarization**: Context-aware summaries in original language
- **Interactive Chat**: Conversational interface with video content
- **Multi-language Support**: Automatic language detection and processing

### 🌐 Website Content Analysis
- **Smart Scraping**: Comprehensive website content extraction
- **Deep Link Processing**: Automatic discovery and processing of related pages
- **Content Structuring**: Organized extraction of textual information
- **Summary Generation**: Key insights and main points extraction
- **Conversational Interface**: Chat with website content

### 📄 Document Processing
- **Multi-format Support**: PDF, DOCX, and TXT file processing
- **Text Extraction**: Robust text extraction with encoding handling
- **Vector Embeddings**: Advanced semantic search capabilities
- **Document Chat**: Interactive Q&A with document content
- **Summary Generation**: Comprehensive document summaries

### 🔧 Advanced Features
- **RAG Implementation**: Retrieval-Augmented Generation for accurate responses
- **Vector Search**: FAISS-powered similarity search
- **Conversation Memory**: Persistent chat history across sessions
- **Error Handling**: Robust error management and user feedback
- **Responsive UI**: Modern, mobile-friendly Streamlit interface

## 🛠 Technologies Used

### **Core Framework**
- **[Streamlit](https://streamlit.io/)**: Modern web application framework
- **[Python 3.8+](https://python.org/)**: Primary programming language

### **AI & Machine Learning**
- **[OpenAI GPT-4](https://openai.com/)**: Large language model for chat and summarization
- **[OpenAI Whisper](https://openai.com/whisper/)**: Advanced speech recognition
- **[LangChain](https://python.langchain.com/)**: LLM application development framework
- **[FAISS](https://faiss.ai/)**: Vector similarity search and clustering

### **Data Processing**
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: YouTube content extraction
- **[PyPDF2](https://pypdf2.readthedocs.io/)**: PDF processing
- **[python-docx](https://python-docx.readthedocs.io/)**: DOCX document handling
- **[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)**: Web scraping

### **Vector Operations**
- **[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)**: Text vectorization
- **[RecursiveCharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter)**: Intelligent text chunking

### **Key Components**

1. **Content Processors**: Modular processors for different content types
2. **Vector Store**: FAISS-based similarity search engine
3. **RAG Pipeline**: Retrieval-Augmented Generation system
4. **Memory Management**: Conversation context preservation
5. **User Interface**: Responsive Streamlit web application

## 📥 Installation

### **Prerequisites**
- Python 3.9 or higher
- OpenAI API key
- FFmpeg (for audio processing)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/AhmedYusri54/Mulitmodal-AI-Educational.git
cd multimodal-ai-educational
```

### **Step 2: Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Install System Dependencies**

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## ⚙️ Configuration

### **Environment Setup**
Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### **Requirements File**
Create a `requirements.txt` file:

```txt
streamlit>=1.28.0
openai>=1.0.0
langchain>=0.1.0
langchain-openai>=0.0.5
python-dotenv>=1.0.0
yt-dlp>=2023.11.16
PyPDF2>=3.0.1
python-docx>=0.8.11
faiss-cpu>=1.7.4
beautifulsoup4>=4.12.2
requests>=2.31.0
```

## 🚀 Usage

### **Starting the Application**
```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### **Processing Content**

#### **YouTube Videos**
1. Navigate to the "Process Video" tab
2. Enter a YouTube URL
3. Click "Process Video"
4. View transcript and summary
5. Switch to "Chat with Video" for interactive Q&A

#### **Websites**
1. Go to "Process Website" tab
2. Enter website URL
3. Click "Process Website"
4. Review extracted content and summary
5. Use "Chat with Website" for questions

#### **Documents**
1. Open "Process Document" tab
2. Upload PDF, DOCX, or TXT file
3. Click "Process Document"
4. Read extracted text and summary
5. Chat with document content in dedicated tab

### **Interactive Features**
- **Real-time Chat**: Ask questions about processed content
- **Conversation History**: View previous interactions
- **Reset Conversations**: Clear chat history when needed
- **Multi-language Support**: Automatic language detection

## 📚 API Reference

### **Core Classes**

#### `YouTubeProcessor`
```python
class YouTubeProcessor:
    def process_video(self, youtube_url: str) -> dict
    def chat_with_video(self, question: str) -> str
    def reset_conversation(self) -> str
```

#### `WebsiteProcess`
```python
class WebsiteProcess:
    def process_website(self, url: str) -> tuple
    def chat_with_website_content(self, question: str) -> str
    def reset_website_conversation(self) -> str
```

#### `DocumentProcessor`
```python
class DocumentProcessor:
    def process_document(self, file_path: str) -> tuple
    def chat_with_document(self, question: str) -> str
    def reset_document_conversation(self) -> str
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

### **Code Standards**
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Common Issues**

**Issue**: `docx` import error
**Solution**: Install python-docx: `pip install python-docx`

**Issue**: FFmpeg not found
**Solution**: Install FFmpeg system-wide

**Issue**: OpenAI API errors
**Solution**: Check API key and usage limits

### **Performance Tips**
- Use shorter videos for faster processing
- Ensure stable internet connection for web scraping
- Monitor OpenAI API usage to avoid rate limits
- Clear conversation history periodically

---

<div align="center">

**Made with ❤️ by [Ahmed Yusri]**

⭐ **Star this repository if you find it helpful!** ⭐

</div>
