from __future__ import annotations

import argparse
import base64
import mimetypes
import sys
import traceback
from pathlib import Path

import llama_cpp
from llama_cpp import Llama


def image_payload(path: Path) -> dict:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")

    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime_type};base64,{encoded}",
        },
    }


def audio_payload(path: Path) -> dict:
    audio_format = path.suffix.lower().lstrip(".")

    if audio_format not in {"wav", "mp3"}:
        raise ValueError(
            f"Use a WAV or MP3 file for this reproduction, got: {path.suffix}"
        )

    encoded = base64.b64encode(path.read_bytes()).decode("ascii")

    return {
        "type": "input_audio",
        "input_audio": {
            "data": encoded,
            "format": audio_format,
        },
    }


def build_messages(kind: str, media_path: Path, request_number: int) -> list[dict]:
    if kind == "image":
        media = image_payload(media_path)
        instruction = (
            f"This is independent request {request_number}. "
            "Describe the image briefly."
        )
    else:
        media = audio_payload(media_path)
        instruction = (
            f"This is independent request {request_number}. "
            "Transcribe the audio briefly."
        )

    return [
        {
            "role": "user",
            "content": [
                media,
                {
                    "type": "text",
                    "text": instruction,
                },
            ],
        }
    ]


def response_text(response: dict) -> str:
    return response["choices"][0]["message"]["content"]


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--mmproj", type=Path, required=True)
    parser.add_argument("--media", type=Path, required=True)
    parser.add_argument("--kind", choices=("image", "audio"), required=True)
    parser.add_argument("--n-ctx", type=int, default=8192)
    parser.add_argument(
        "--workaround",
        action="store_true",
        help="After reset(), also clear the target context memory explicitly.",
    )
    args = parser.parse_args()

    for path in (args.model, args.mmproj, args.media):
        if not path.is_file():
            raise FileNotFoundError(path)

    print(f"Python: {sys.version}")
    print(f"llama-cpp-python: {llama_cpp.__version__}")
    print(f"Package: {llama_cpp.__file__}")
    print(f"Model: {args.model.resolve()}")
    print(f"MMProj: {args.mmproj.resolve()}")
    print(f"Media: {args.media.resolve()}")
    print(f"Kind: {args.kind}")
    print(f"Workaround: {args.workaround}")

    llm = None

    try:
        # Model construction: exactly once.
        print("\n[1/5] Loading model once")
        llm = Llama(
            model_path=str(args.model.resolve()),
            mmproj_path=str(args.mmproj.resolve()),
            n_gpu_layers=-1,
            n_ctx=args.n_ctx,
            verbose=True,
            verbosity=2,
            chat_handler_kwargs={
                "verbose": True,
            },
        )

        print("\n[2/5] Running first request")
        first = llm.create_chat_completion(
            messages=build_messages(args.kind, args.media, 1),
            max_tokens=32,
            temperature=0.0,
        )
        print(f"First response: {response_text(first)!r}")
        print(f"n_tokens after first request: {llm.n_tokens}")

        # Explicit reset: exactly once.
        print("\n[3/5] Calling llm.reset() exactly once")
        llm.reset()
        print(f"n_tokens immediately after reset: {llm.n_tokens}")

        if args.workaround:
            print("[control] Calling llm._ctx.memory_clear(True)")
            llm._ctx.memory_clear(True)

            checkpoint_manager = getattr(llm, "_hybrid_cache_mgr", None)
            if checkpoint_manager is not None:
                print("[control] Clearing hybrid checkpoint manager")
                checkpoint_manager.clear()

        print("\n[4/5] Running independent second request")
        second = llm.create_chat_completion(
            messages=build_messages(args.kind, args.media, 2),
            max_tokens=32,
            temperature=0.0,
        )
        print(f"Second response: {response_text(second)!r}")

        print("\nRESULT: second independent request succeeded")
        return 0

    except Exception:
        print("\nRESULT: request failed")
        traceback.print_exc()
        return 1

    finally:
        # Model close: exactly once.
        if llm is not None:
            print("\n[5/5] Closing model once")
            llm.close()


if __name__ == "__main__":
    raise SystemExit(main())