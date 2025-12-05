#!/usr/bin/env bash

# Exit on first error
set -e

# List of Ollama model names exactly as shown on ollama.com
models=(
  "mistral"          # or "mistral:latest" if that's the tag shown
  "gemma3"           # adjust if page shows e.g. "gemma2:2b"
  "ministral-3:8b"
  "llama3.1:8b"
  "qwen3"            # or "qwen2.5-coder" etc.
)

for m in "${models[@]}"; do
  echo "Pulling $m..."
  ollama pull "$m" || echo "⚠️  Failed to pull $m"
done

echo "All models pulled (or attempted)!"