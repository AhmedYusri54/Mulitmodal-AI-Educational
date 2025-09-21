from webscraping_base import Website, get_links
import openai
from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class WebsiteProcess:
    def __init__(self):
      self.embeddings = None
      self.vector_store = None
      self.conversation_chain = None
      self.memory = None
      self.MODEL = "gpt-4o-mini"

    def load_models(self):
      if self.embeddings is None:
        self.embeddings = OpenAIEmbeddings()

    def get_all_details(self, url):
      result = "Landing page:\n"
      result += Website(url).get_contents()
      links = get_links(url)
      print("Found links:", links)
      for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
      return result

    def create_website_vector_store(self, text: str):
        """Create FAISS vector store from website text"""
        self.load_models()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]

        self.vector_store = FAISS.from_documents(documents, self.embeddings)

        self.setup_website_conversation_chain()

        return self.vector_store

    def setup_website_conversation_chain(self):
        """Setup the conversational retrieval chain for documents"""
        if self.vector_store is not None:
            llm = ChatOpenAI(temperature=0.7, model_name=self.MODEL)
            self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
            retriever = self.vector_store.as_retriever()
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                memory=self.memory
            )

    def generate_website_summary(self, text: str):
        """Generate summary for document using OpenAI GPT"""
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful assistant that creates comprehensive summaries of Website contents.

                        IMPORTANT INSTRUCTIONS:
                        1. Analyze the language of the provided website content
                        2. Write the summary in the SAME LANGUAGE as the website content
                        3. If the document is in Arabic, write the summary in Arabic
                        4. If the document is in English, write the summary in English
                        5. And so on for any other language

                        Create a well-structured summary that includes:
                        - Main topic and purpose of the document
                        - Key points and sections
                        - Important details and findings
                        - Conclusions or recommendations
                        - Provide links to related content if available

                        Keep the summary comprehensive but concise."""
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze this document and provide a comprehensive summary in the same language as the website content:\n\n{text}..."
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating website summary: {str(e)}"

    def chat_with_website_content(self, question: str):
        """Chat with the Website content using conversational retrieval"""
        if self.conversation_chain is None:
            return "No Website content processed yet. Please process a url first."

        try:
            response = self.conversation_chain({"question": question})
            return response['answer']
        except Exception as e:
            return f"Error in website conversation: {str(e)}"

    def reset_website_conversation(self):
        """Reset the Website conversation memory"""
        if self.memory is not None:
            self.memory.clear()
            return "Website conversation history cleared!"
        return "No website conversation to reset."

    def process_website(self, url: str):
        try:
            text = self.get_all_details(url)

            self.processed_document_text = text
            self.create_website_vector_store(text)
            summary = self.generate_website_summary(text)
            return text, summary, "Website processed successfully!"

        except Exception as e:
            return "", "", f"Error processing website: {str(e)}"
