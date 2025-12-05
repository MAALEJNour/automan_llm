#!/bin/bash
set -e

echo "Installing Ollama for Linux..."

curl -fsSL https://ollama.com/install.sh | sh

echo "Ollama installed!"
ollama --version