#!/bin/bash
set -e

echo "Installing Ollama for macOS..."

brew update
brew install ollama || brew upgrade ollama

echo "Ollama installed!"
ollama --version