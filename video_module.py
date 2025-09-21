import os
import yt_dlp
import openai
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import re
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class YouTubeProcessor:
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.conversation_chain = None
        self.memory = None
        self.MODEL = "gpt-4o-mini"
        self.AUDIO_MODEL = "whisper-1"
    def load_models(self):
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()

    def extract_video_id(self, url) -> str:
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\n?#]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^&\n?#]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("Invalid YouTube URL")

    def download_audio(self, youtube_url):
        video_id = self.extract_video_id(youtube_url)
        permanent_path = f"temp_audio_{video_id}.mp3"
        output_template = f"temp_audio_{video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template + '.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            if os.path.exists(permanent_path):
                return permanent_path
            else:
                import glob
                matching_files = glob.glob(f"temp_audio_{video_id}.*")
                if matching_files:
                    os.rename(matching_files[0], permanent_path)
                    return permanent_path
                else:
                    raise FileNotFoundError(f"Downloaded audio file not found for video {video_id}")

        except Exception as e:
            import glob
            for file in glob.glob(f"temp_audio_{video_id}*"):
                try:
                    os.remove(file)
                except:
                    pass
            raise e

    def transcribe_audio(self, audio_path):
        audio_file = open(audio_path, "rb")
        transcription = openai.audio.transcriptions.create(model=self.AUDIO_MODEL, file=audio_file, response_format="text")
        return transcription

    def create_vector_store(self, text, progress_callback=None):
        if progress_callback:
            progress_callback(0.7, "Creating vector embeddings...")

        self.load_models()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )

        chunks = text_splitter.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.setup_conversation_chain()

        return self.vector_store

    def setup_conversation_chain(self):
        if self.vector_store is not None:
            llm = ChatOpenAI(temperature=0.7, model_name=self.MODEL)
            self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
            retriever = self.vector_store.as_retriever()
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                memory=self.memory
            )

    def generate_summary(self, text: str):
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                    {
                        "role": "system",
                        "content": """ You are a helpful assistant that creates comprehensive summaries of video transcripts.

                        IMPORTANT INSTRUCTIONS:
                        1. Analyze the language of the provided transcript
                        2. Write the summary in the SAME LANGUAGE as the transcript
                        3. If the transcript is in Arabic, write the summary in Arabic
                        4. If the transcript is in English, write the summary in English
                        5. If the transcript is in Spanish, write the summary in Spanish
                        6. And so on for any other language

                       s: Create a well-structured summary that include
                        - Main topic and purpose of the video
                        - Key points discussed
                        - Important details and examples
                        - Conclusions or takeaways

                        Keep the summary comprehensive but concise, and maintain the same tone and formality level as the original content."""
                    },
                    {
                        "role": "user",
                        "content": f"Please provide a comprehensive summary using the same language of the following video transcript:\n\n{text[:4000]}..."
                    }
            ],
            max_tokens=300,
            temperature=0.7
            )
        return response.choices[0].message.content

    def chat_with_video(self, question: str):
        if self.conversation_chain is None:
            return "No video processed yet. Please process a video first."

        response = self.conversation_chain({"question": question})
        return response['answer']

    def reset_conversation(self):
        if self.memory is not None:
            self.memory.clear()
            return "Conversation history cleared!"
        return "No conversation to reset."

    def process_video(self, youtube_url: str):
      video_id = self.extract_video_id(youtube_url)
      audio_path = self.download_audio(youtube_url)
      transcript = self.transcribe_audio(audio_path)
      self.create_vector_store(transcript)
      summary = self.generate_summary(transcript)
      if os.path.exists(audio_path):
        os.remove(audio_path)
        return {
            "video_id": video_id,
            "transcript": transcript,
            "summary": summary
        }