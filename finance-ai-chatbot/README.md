# Finance AI Chatbot
This financial AI chatbot provides real-time market updates, personalized banking support, and fraud detection to help users stay informed and secure. It analyzes investment portfolios, offering optimized recommendations for better asset management. Additionally, it maintains a chat history to track previous inquiries, ensuring a seamless and personalized user experience.

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
   cd finance-ai-chatbot
   python -m venv venv
   pip install -r requirements.txt
```

## Configuration
- LLM:
   - [furiosa-ai/Llama-3.1-8B-Instruct](https://huggingface.co/furiosa-ai/Llama-3.1-8B-Instruct) 
   - [furiosa-ai/DeepSeek-R1-Distill-Llama-8B](https://huggingface.co/furiosa-ai/DeepSeek-R1-Distill-Llama-8B)
- AI Framework: 
   - LangChain 0.3.25

 
## Usage
Execute the `.py` file using the command below to test the recipe and interact with the Multi-Model Routing Chatbot. You can ask any question, and the chatbot will decide which LLM to use for the response.

```
python app.py
```

## File Structure

```
financial_chatbot/
│── app.py                        # FastAPI server
│── finance_chatbot.py             # AI chatbot logic
│── financial_tools.py             # Banking and investment utilities
│── sentiment_analysis.py          # Sentiment analysis for response optimization
│── chat_history.json              # User chat history
│── requirements.txt               # Required dependencies
```
