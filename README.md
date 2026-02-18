# llmwrap

Lightweight adapter for LLM chat completions — text, images, PDFs/files.  
OpenAI-compatible (works great with OpenRouter, Anthropic via compat layer, etc.).

## Installation

```bash
pip install amyrmahdy-llmwrap
# or
uv add amyrmahdy-llmwrap
```

## Quick start
```python
from amyrmahdy_llmwrap import LLM

llm = LLM(
    api_key="sk-...",
    base_url="https://openrouter.ai/api/v1",
    model="anthropic/claude-3.5-sonnet",
)

# Text
print(llm.complete([{"role": "user", "content": "Hi!"}]))

# Image + text
messages = [
    {"role": "user", "content": [
        LLM.text_content("Describe this."),
        LLM.image_content("photo.jpg"),
    ]}
]
print(llm.complete(messages))
```