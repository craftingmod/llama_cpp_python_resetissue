uv python install 3.13
uv venv --python 3.13 .venv

$python = Resolve-Path .\.venv\Scripts\python.exe

uv pip install --python $python `
  "https://github.com/JamePeng/llama-cpp-python/releases/download/v0.3.46-cu130-win-20260808/llama_cpp_python-0.3.46+cu130-cp313-cp313-win_amd64.whl"