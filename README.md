## llama-cpp-python reset() reproduce

1. Setup environment via `make-env.ps1`
2. Fetch model via `fetch-model.ps1`
3. `reproduce.ps1` for reproduce.

## Issue

`llm.reset()` only reset `n_tokens` to 0, but context memory is still left, including KV/SWA state.

## Error log

```
GenericMTMDChatHandler(__call__): Evaluating TEXT chunk (88 tokens) at pos 0...

RESULT: request failed
Traceback (most recent call last):
  File "<workspace>\.venv\Lib\site-packages\llama_cpp\llama.py", line 1292, in eval
    status = self._ctx.decode(self._batch)
  File "<workspace>\Python\llama-cpp-python-reset\.venv\Lib\site-packages\llama_cpp\_internals.py", line 837, in decode
    raise RuntimeError(f"llama_decode failed (code {return_code}): {msg}")
RuntimeError: llama_decode failed (code -1): Invalid input batch (e.g. n_tokens == 0 or exceeding capacity)
  ...
  File "<workspace>\.venv\Lib\site-packages\llama_cpp\llama.py", line 1319, in eval
    raise RuntimeError(f"Llama.eval(decode): Fatal Decode Error at Pos {self.n_tokens}, "
                       f"Batch size {current_batch_size}, chunk[:{min_pos}]={preview}: {str(e)}") from e
RuntimeError: Llama.eval(decode): Fatal Decode Error at Pos 0, Batch size 88, chunk[:88]=[2, 105, 9731, 107, 3048, 659, 614, 47321, 11844, 236764, 18997, 236764, 532, 11045, 151359, 12498, 16326, 600, 123552, 657, 19297, 6611, 532, 112353, 22454, 4876, 236764, 28494, 236764, 29981, 236764, 1816, 528, 4876, 236764, 18583, 236764, 532, 1027, 7426, 3004, 236764, 1651, 992, 38020, 1418, 2934, 23704, 236764, 8207, 236764, 532, 2918, 236772, 2003, 236772, 9340, 1056, 6780, 2192, 2462, 35136, 528, 506, 1638, 5192, 618, 506, 2430, 236789, 236751, 2934, 236764, 9866, 54651, 236764, 5707, 236764, 532, 160022, 11045, 236761, 106, 107, 105, 2364, 107, 255999]: llama_decode failed (code -1): Invalid input batch (e.g. n_tokens == 0 or exceeding capacity)
```