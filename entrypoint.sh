#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "Retrieve LLAMA3 model..."
ollama pull qwen3:4b
ollama pull qwen3-embedding:4b
echo "Done!"

# Wait for Ollama process to finish.
wait $pid