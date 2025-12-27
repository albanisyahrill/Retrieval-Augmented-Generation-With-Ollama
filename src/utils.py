from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableBinding
from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src import logging

logger = logging.getLogger(__name__)

class CreatingRAGPipeline:
    @staticmethod
    def get_pdf_text(pdf_docs_path: str) -> str:
        """
        This function extracts text from PDF documents.
        """
        try:
            logger.info("Extracting text from PDF documents.")
            text = ''
            if isinstance(pdf_docs_path, str):
                pdf_reader = PdfReader(pdf_docs_path)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            elif isinstance(pdf_docs_path, list):
                for pdf in pdf_docs_path:
                    pdf_reader = PdfReader(pdf)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            
            logger.info("Text extraction completed.")
            return text
        except Exception as e:
            logger.error(f"Error when extracting text from PDF documents: {e}")
            raise
    
    @staticmethod
    def get_text_chunks(text: str, chunk_size=600, chunk_overlap=250) -> list:
        """
        This function splits text into chunks.
        """
        try:
            logger.info("Splitting text into chunks.")
            
            # Initialize the RecursiveCharacterTextSplitter with specified chunk size and overlap
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            
            # Split the combined text into smaller chunks
            texts = text_splitter.split_text(text)
            logger.info(f"Text split into {len(texts)} chunks.")
            return texts
        except Exception as e:
            logger.error(f"Error when splitting text into chunks: {e}")
            raise

    @staticmethod
    def get_vector_db(text_chunks: list, embedder: OllamaEmbeddings) -> VectorStore:
        """
        This function creates a vector database from text chunks.
        """
        try:
            logger.info("Creating vector database from text chunks.")
            vector_db = FAISS.from_texts(text_chunks, embedder)
            logger.info("Vector database created successfully.")
            return vector_db
        except Exception as e:
            logger.error(f"Error when creating vector database: {e}")
            raise

    @staticmethod
    def get_retrieval_chain(vector_db: VectorStore, llm: OllamaLLM) -> RunnableBinding:
        """
        This function sets up a retrieval chain.
        """
        try:
            logger.info("Setting up retrieval chain.")
            
            # Create retriever from vector database with top k=3
            retriever = vector_db.as_retriever(search_kwargs={"k": 3})

            # Define the prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "Gunakan context berikut untuk menjawab pertanyaan di akhir. Jika Anda tidak tahu jawabannya, cukup katakan \"Maaf, saya tidak tahu\", jangan mencoba membuat jawaban yang tidak relevan. Jawablah dengan lengkap dan sejelas mungkin. Selalu katakan \"Terima kasih sudah bertanya!\" di akhir jawaban. Jawab full dengan bahasa indonesia. <context> {context} </context>"),
                ("human", "{input}"),
            ])
            
            # Create combine documents chain
            combine_docs_chain = create_stuff_documents_chain(
                llm, prompt_template
            )
            
            # Create retrieval chain
            retrieval_chain = create_retrieval_chain(combine_docs_chain=combine_docs_chain,retriever=retriever)
            logger.info("retrieval chain set up successfully.")
            return retrieval_chain
        except Exception as e:
            logger.error(f"Error when setting up retrieval chain: {e}")
            raise