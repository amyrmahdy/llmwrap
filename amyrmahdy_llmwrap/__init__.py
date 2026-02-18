from importlib.metadata import version

import base64
from pathlib import Path
from typing import Any, List, Dict, Literal, Union

from openai import OpenAI


__version__ = version("amyrmahdy_llmwrap")


class LLM:
    def __init__(
            self,
            api_key: str,
            model: str = "gpt-4o-mini",
            base_url: str = "https://openrouter.ai/api/v1",
            **client_kwargs: Any,
    ):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            **client_kwargs,
        )
        self.model = model

    def complete(
            self,
            messages: List[Dict[str, Any]],
            max_tokens: int = 4096,
            temperature: float = 0.1,
            **kwargs
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    @staticmethod
    def text_content(text: str) -> Dict[str, str]:
        return {"type": "text", "text": text}

    @staticmethod
    def image_content(
            source: Union[str, Path, bytes],
            detail: Literal["low", "high", "auto"] = "auto"
    ) -> Dict[str, str]:

        if isinstance(source, (str, Path)) and not str(source).startswith(("http://"), ("https://")):
            path = Path(source)
            if not path.is_file():
                raise FileNotFoundError(source)
            mime = "image/jpeg"
            if path.suffix.lower() in {".png"}:
                mime = "image/png"
            elif path.suffix.lower() in {".webp"}:
                mime = "image/webp"

            b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
            url = f"data:{mime};base64,{b64}"

        elif isinstance(source, bytes):
            b64 = base64.b64encode(source).decode("utf-8")
            url = f"data:image/jpeg;base64,{b64}"

        else:
            url = str(source)

        return {"type": "image", "url": url}

    @staticmethod
    def file_content(
            source: Union[str, Path, bytes],
            mime_type: str = "application/pdf",
            filename: str | None = None,
    ) -> Dict[str, Any]:
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {path}")
            data = path.read_bytes()
            filename = filename or path.name
        elif isinstance(source, bytes):
            data = source
            filename = filename or "uploaded_file"
        else:
            raise ValueError("source must be path-like, str (url/path), or bytes")

        b64 = base64.b64encode(data).decode("utf-8")
        file_data = f"data:{mime_type};base64,{b64}"

        return {
            "type": "file",
            "file": {
                "filename": filename,
                "file_data": file_data,
            },
        }

