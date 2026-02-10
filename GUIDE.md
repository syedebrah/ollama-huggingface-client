# Complete Guide: Hugging Face to Ollama

A step-by-step guide to download GGUF models from Hugging Face and run them in Ollama.

---

## Prerequisites

1. **Install UV** (Python package manager)
   ```bash
   # Download and install from: https://github.com/astral-sh/uv
   ```

2. **Install Ollama**
   ```bash
   # Download from: https://ollama.ai
   ```

3. **Install Hugging Face CLI**
   ```bash
   uv tool install huggingface_hub[cli]
   ```

---

## Step 1: Download GGUF Model from Hugging Face

### Find a GGUF Model
- Go to [Hugging Face](https://huggingface.co)
- Search for models with "GGUF" in the name
- Example: `TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF`

### Download the Model
```bash
hf download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

**Output**: Shows the path where the model is downloaded
```
C:\Users\<username>\.cache\huggingface\hub\models--TheBloke--TinyLlama-1.1B-Chat-v1.0-GGUF\snapshots\...\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

---

## Step 2: Create a Modelfile

Create a file named `Modelfile` (no extension) with this content:

```plaintext
FROM C:/Users/<username>/.cache/huggingface/hub/models--TheBloke--TinyLlama-1.1B-Chat-v1.0-GGUF/snapshots/<hash>/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

SYSTEM You are a helpful AI assistant.

PARAMETER temperature 0.1
PARAMETER top_p 0.9
PARAMETER top_k 40
```

### Important Notes
- ✅ Use **forward slashes** (`/`) in the path, even on Windows
- ✅ Replace `<username>` and `<hash>` with your actual values
- ✅ First line MUST start with `FROM`

---

## Step 3: Create the Model in Ollama

```bash
ollama create tiny_model -f .\Modelfile
```

**Expected output**:
```
gathering model components
copying file sha256:...
writing manifest
success
```

---

## Step 4: Verify the Model

```bash
ollama list
```

You should see your model:
```
NAME                 ID              SIZE
tiny_model:latest    df57b491f48a    668 MB
```

---

## Step 5: Use the Model

### Option A: Command Line
```bash
ollama run tiny_model
```

### Option B: Python Code

**Install requests:**
```bash
uv pip install requests
```

**Create `main.py`:**
```python
import requests

def chat_with_ollama(prompt, model="tiny_model:latest"):
    """Ask Ollama a question and get a response."""
    
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "top_k": 40,
        }
    }
    
    try:
        print(f"🤖 Sending to {model}...")
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "No response")
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    answer = chat_with_ollama("What is AI in one sentence?")
    print(answer)
```

**Run it:**
```bash
uv run python main.py
```

---

## Common Issues & Solutions

### Issue 1: "command must be one of..."
**Problem**: Modelfile syntax error

**Solution**: Make sure first line starts with `FROM`

### Issue 2: "no Modelfile or safetensors files found"
**Problem**: Path uses backslashes or is incorrect

**Solution**: Use forward slashes (`/`) in the path

### Issue 3: "bind: Only one usage of each socket"
**Problem**: Ollama is already running (this is good!)

**Solution**: No action needed, continue with next steps

### Issue 4: "404 Client Error"
**Problem**: Model doesn't exist or was deleted

**Solution**: Check available models with `ollama list`

---

## Anti-Hallucination Parameters

These parameters reduce hallucination (making up false information):

| Parameter | Value | Effect |
|-----------|-------|--------|
| `temperature` | 0.1 | Low = more factual, less creative |
| `top_p` | 0.9 | Focus on most probable tokens |
| `top_k` | 40 | Limit vocabulary choices |

**For different use cases:**
- **Factual answers**: temperature = 0.0 - 0.2
- **Code generation**: temperature = 0.1 - 0.3
- **Creative writing**: temperature = 0.7 - 1.0

---

## Quick Reference

### Essential Commands
```bash
# Download model
hf download <repo>/<model-name> <file.gguf>

# Create Ollama model
ollama create <model-name> -f .\Modelfile

# List models
ollama list

# Run model
ollama run <model-name>

# Delete model
ollama rm <model-name>
```

### File Structure
```
project/
├── Modelfile          # Ollama configuration
├── main.py           # Python client
└── test.py           # Simple test script
```

---

## Complete Example Workflow

```bash
# 1. Install tools
uv tool install huggingface_hub[cli]

# 2. Download model
hf download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 3. Create Modelfile (copy path from step 2)
notepad Modelfile

# 4. Create Ollama model
ollama create tiny_model -f .\Modelfile

# 5. Test it
ollama run tiny_model

# 6. Use in Python
uv pip install requests
uv run python main.py
```

---

## Tips

1. **Choose smaller models first** (1B-7B parameters) for faster responses
2. **GGUF quantization levels**:
   - `Q4_K_M` - Good balance (recommended)
   - `Q5_K_M` - Better quality, larger size
   - `Q8_0` - Best quality, largest size
3. **Model naming**: Use descriptive names like `tiny_model`, `code_model`, etc.
4. **Keep models organized**: Delete unused models with `ollama rm <name>`

---

## Resources

- [Hugging Face Models](https://huggingface.co/models)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [GGUF Format Info](https://github.com/ggerganov/ggml)
