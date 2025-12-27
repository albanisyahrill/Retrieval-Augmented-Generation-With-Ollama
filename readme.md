## Architecture Overview

![RAG-Architecture](./architecture/RAG-Archicecture.jpg)

## Installation & Setup

### Prerequisites

- Docker & Docker Compose
- Git
- Python 3.12+ (for local development)

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Setup Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env with appropriate values
```

### 3. Create Docker Network

```bash
docker network create llm-networks
```

### 4. Run Services

```bash
# Run all services
docker compose up ollama -d # Waiting for the model are successfully pulled

# After the model successfully pulled, run command below
docker compose up fastapi_app -d
```

---

## Design Decisions

- Using Langchain and Ollama
- Langchain are famous orchestration framework to simplify building llm application
- Ollama are the open source platform for running llm locally

## Trade-Offs

- The model ollama provide are the model that already quantizated, so the model size will be lightweight and running efficiently on local machines
- Ollama offering privacy, because it running on local machine
- When you've done downloaded the model, it will still run even if you don't connect to internet
- But you still need a mid-high computer, because the llm running locally and it's different if you use OpenAI, which only requires an API key to access the model

## Limitations

- Can't access full model, because model that Ollama provide has been quantized, so it doesn't fit for experiment or research
- Still need mid-high computer due to llm running locally

## Future Improvements

- Applying multithreading if possible
- Writing the documentation (commentar dan docstring) more comprehensive
- Automation to running the service at docker compose, so developer doesn't wait for model successfully pulled and after that run the fastapi_app service
