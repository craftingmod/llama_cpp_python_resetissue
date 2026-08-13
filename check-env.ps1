. "$PSScriptRoot\.venv\Scripts\Activate.ps1"

& python -c "import sys, llama_cpp; print(sys.version); print(llama_cpp.__version__); print(llama_cpp.__file__)"
nvidia-smi

pause