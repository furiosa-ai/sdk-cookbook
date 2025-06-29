# Routing workflows

This guide introduces a simple chatbot built with an adaptive query routing strategy. By dynamically routing questions to different LLMs based on complexity, it balances speed and accuracy. Tailored prompts ensure efficient responses, leveraging lightweight models for simple queries and stronger models for challenging ones.

## Prerequisites
If you have access to the FurisoaAI LLM API endpoint or a dedicated RNGD server, the only step you need to take before beginning the SDK cookbook is installing the necessary prerequisites for the FuriosaAI SDK stack. Please refer to the provided page to choose and set up your preferred version of the FuriosaAI SDK. Currently, this SDK cookbook is based on FuriosaAI SDK version 2025.3.0.
- [Install Prerequisites for FuriosaAI SDK](https://developer.furiosa.ai/latest/en/getting_started/prerequisites.html)

## Set Environments 

### Requirements
- FuriosaSDK 2025.3.0
- RNGD server or Endpoint API

### Installation
```
   git clone https://github.com/furiosa-ai/sdk-cookbook.git
   cd agentic_workflows/routing
   python -m venv venv
   pip install -r requirements.txt
```

## Configuration
- LLM:
   - [furiosa-ai/Llama-3.1-8B-Instruct](https://huggingface.co/furiosa-ai/Llama-3.1-8B-Instruct)

 
## Usage
For reference, pre-generated outputs are available in the accompanying `.ipynb` notebook.
```
python routing.py
```