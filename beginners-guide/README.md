# Beginners Guide

This guide offers a starting point for working with the FuriosaAI SDK in large language model (LLM) applications. Aimed at beginners, it describes the essential setup and quick usage method needed to begin development. It covers:
- How to perform LLM inference using the FuriosaAI SDK
- How to build AI agents by integrating tool calling functionality with the SDK

## Prerequisites
If you have access to the FurisoaAI LLM API endpoint or a dedicated RNGD server, the only step you need to take before beginning the SDK cookbook is installing the necessary prerequisites for the FuriosaAI SDK stack. Please refer to the provided page to choose and set up your preferred version of the FuriosaAI SDK. Currently, this SDK cookbook is based on FuriosaAI SDK version 2025.02.
- [Install Prerequisites for FuriosaAI SDK](https://developer.furiosa.ai/latest/en/getting_started/prerequisites.html)

## Set Environments 

### Requirements
- FuriosaSDK 2025.02
- RNGD server or Endpoint API

### Installation
```
   git clone https://github.com/furiosa-ai/sdk-cookbook.git
   cd beginners-guide
   python -m venv venv
   pip install -r requirements.txt
```

## Configuration
- LLM:
   - [furiosa-ai/Llama-3.1-8B-Instruct](https://huggingface.co/furiosa-ai/Llama-3.1-8B-Instruct)

 
## Usage
For reference, pre-generated outputs are available in the accompanying `.ipynb` notebook.

