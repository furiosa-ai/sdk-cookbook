# Simple RAG
This recipe will guide you through the process of building a Retrieval-Augmented Generation (RAG) system. It starts with scraping documents from the web and proceeds to creating a vector database. Finally, it covers generating answers using a large language model (LLM) based on documents retrieved in response to a user question.

## Prerequisites
If you have access to the FurisoaAI LLM API endpoint or a dedicated RNGD server, the only step you need to take before beginning the SDK cookbook is installing the necessary prerequisites for the FuriosaAI SDK stack. Please refer to the provided page to choose and set up your preferred version of the FuriosaAI SDK. Currently, this SDK cookbook is based on FuriosaAI SDK version 2025.3.0.
- [Install Prerequisites for FuriosaAI SDK](https://developer.furiosa.ai/latest/en/getting_started/prerequisites.html)

## Set Environments 

### Requirements
- FuriosaSDK 2025.3.0
- RNGD server or Endpoint API
- OpenAI API Key 

### Installation
```
   git clone https://github.com/furiosa-ai/sdk-cookbook.git
   cd simple-rag
   python -m venv venv
   pip install -r requirements.txt

```

### Setup

```
   # set vector db
   bash bash_scripts/setup-pgvector.sh
   
   # OPENAI_API for embedding model
   export OPENAI_API_BASE="https://api.openai.com/v1"
   export OPENAI_API_KEY=<your-openai-api-key>

```

## Configuration
- Embedding model: `text-embedding-ada-002`

- LLM: [EXAONE-3.5-32B-Instruct](https://huggingface.co/furiosa-ai/EXAONE-3.5-32B-Instruct)

- LLM Adapter: LightLLM or OpenAI
- VectorDB : PGVector
## Usage
```
# If you need to set some configurations regarding RAG modeling, such as chunk size, model context length, or model to use, then visit the `experiment_config.py` change as you want.

python main.py
```

## References

This recipes is adapted from https://github.com/ray-project/llm-applications/blob/main/notebooks/rag.ipynb
