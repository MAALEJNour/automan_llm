Write-Host "Installing Ollama for Windows..."

Invoke-WebRequest https://ollama.com/download/OllamaSetup.exe -OutFile OllamaSetup.exe
Start-Process -FilePath "./OllamaSetup.exe" -Wait

Write-Host "Ollama installation completed."