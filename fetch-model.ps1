$Gemma4Path = "$PSScriptRoot/gemma-4-E2B-it-Q4_K_M.gguf"
$MmprojPath = "$PSScriptRoot/mmproj-BF16.gguf"

if (!(Test-Path $Gemma4Path) -and !(Test-Path $userfile)) {
  Write-Warning "$userFile absent from both locations"
}

if (!(Test-Path $Gemma4Path)) {
  hf download hf://unsloth/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_K_M.gguf --local-dir ./
}

if (!(Test-Path $MmprojPath)) {
  hf download hf://unsloth/gemma-4-E2B-it-GGUF/mmproj-BF16.gguf --local-dir ./
}
