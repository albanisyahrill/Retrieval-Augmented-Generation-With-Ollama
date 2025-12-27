from dotenv import load_dotenv
import os
from src import logging
from src.llm import LLMMODEL
from src.utils import CreatingRAGPipeline

logger = logging.getLogger(__name__)

load_dotenv()
model_name = os.getenv("LLM_MODEL_NAME")
embedder_model_name = os.getenv("EMBEDDING_MODEL_NAME")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")
pdf_docs_path = os.getenv("DOCS_PATH")

def execute_rag_pipeline():
    """
    This function is pipeline to execute all rag process
    """
    # Initialize LLM and Embeddings
    llm_model = LLMMODEL(model_name=model_name, embedder_model_name=embedder_model_name, base_url=ollama_base_url)

    # Extract text from PDF documents
    text = CreatingRAGPipeline.get_pdf_text(pdf_docs_path)

    # Split text into chunks
    text_chunks = CreatingRAGPipeline.get_text_chunks(text)

    # Create vector database
    vector_db = CreatingRAGPipeline.get_vector_db(text_chunks, llm_model.embedder)

    # Set up conversational retrieval chain
    retrieval_chain = CreatingRAGPipeline.get_retrieval_chain(vector_db, llm_model.llm)

    return vector_db, retrieval_chain
    



