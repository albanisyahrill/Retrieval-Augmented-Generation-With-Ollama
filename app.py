from fastapi import FastAPI
from langchain_core.callbacks import get_usage_metadata_callback
from contextlib import asynccontextmanager
from src.pipeline import execute_rag_pipeline
from src.schemas import UserInput, AnswerResponse
from src import logging

logger = logging.getLogger(__name__)

# Define lifespan event to initialize resources at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize global variables for vector database and retrieval chain
    global vector_db, retrieval_chain
    try:
        # Execute the RAG pipeline to set up the vector database and retrieval chain
        logger.info("Executing RAG pipeline to initialize model...")
        vector_db, retrieval_chain = execute_rag_pipeline()
        logger.info("RAG pipeline executed successfully.")
    except Exception as e:
        logger.error(f"Failed to execute RAG pipeline: {e}")
        raise e
    
    yield
    

app = FastAPI(
    title="RAG PDF QA API",
    description="API untuk tanya jawab dokumen PDF menggunakan Retrieval-Augmented Generation (RAG)",
    lifespan=lifespan
)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "RAG PDF QA API",
        "docs": "/docs"
    }
    
@app.post("/generate_answer", response_model=AnswerResponse,  tags=["RAG"])
async def generate_answer(user_input: UserInput):
    try:
        logger.info(f"Generating answer for query: {user_input.input_prompt}")
        # Generate answer for the example query
        # Using metadata callback to log token usage
        # because ollama return payload doesn't include token usage info
        with get_usage_metadata_callback() as cb:
            response = retrieval_chain.invoke({"input": user_input.input_prompt})
            docs_and_scores = vector_db.similarity_search_with_score(user_input.input_prompt, k=3)
            if cb.usage_metadata:
                for value in cb.usage_metadata.values():
                    input_tokens = value.get('input_tokens', 0)
                    output_tokens = value.get('output_tokens', 0)
                    total_tokens = value.get('total_tokens', 0)
        
        # Prepare and return the response based on the schema
        return AnswerResponse(
            success=True,
            input_prompt=user_input.input_prompt,
            answer=response.get('answer', None),
            docs_and_scores={doc.page_content[:60]: float(f"{score:.4f}") for doc, score in docs_and_scores},
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens
        )
        
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return {"error": str(e)}