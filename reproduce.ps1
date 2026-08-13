. "$PSScriptRoot\.venv\Scripts\Activate.ps1"

python ./reproduce.py --model "./gemma-4-E2B-it-Q4_K_M.gguf" --mmproj "./mmproj-BF16.gguf" --media "./image.png" --kind image

pause