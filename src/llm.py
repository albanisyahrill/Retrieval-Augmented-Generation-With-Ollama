from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_core.runnables.base import RunnableBinding
from src import logging

logger = logging.getLogger(__name__)

class LLMMODEL:
    def __init__(self, model_name: str, embedder_model_name: str, base_url: str):
        logger.info(f"Initializing Ollama LLM with model: {model_name}")
        self.llm = ChatOllama(model=model_name, base_url=base_url, temperature=0.3)
        logger.info("Ollama LLM initialized successfully.")
        
        logger.info("Initializing Ollama Embeddings.")
        self.embedder = OllamaEmbeddings(model=embedder_model_name, base_url=base_url)
        logger.info("Ollama Embeddings initialized successfully.")
    
    def generate_answer(self, prompt: str, retriever: RunnableBinding) -> str:
        try:
            logger.info("Generating answer from LLM.")
            response = retriever.invoke({"input": prompt})
            logger.info("Answer generated successfully.")
            return response
        except Exception as e:
            logger.error(f"Error when generating answer from LLM: {e}")
            raise