
<img src=https://github.com/furiosa-ai/sdk-cookbook/blob/main/docs/images/icon.png width="100"/>



# Furiosa SDK CookBook
A collection of open-source resources and tutorials to help developers seamlessly integrate AI-driven solutions using Furiosa SDK and development tools. Let's explore how AI engineers and researchers can build their own applications using the Furiosa SDK and RNGDs.

## Target audience
This cookbook is for:
- AI engineers: Engineers seeking a quickstart to build production-grade AI applications using Furiosa SDKs.
- AI researchers: Researchers aiming to rapidly prototype AI workflows using Furiosa SDKs.
- AI solution architects: Solution architects looking to efficiently design and implement AI use cases using Furiosa SDKs.


## Prerequisites

If you have access to the FurisoaAI LLM API endpoint or a dedicated RNGD server, the only step you need to take before beginning the SDK cookbook is installing the necessary prerequisites for the Furiosa SDK stack. Please refer to the provided page to choose and set up your preferred version of the FuriosaAI SDK. Currently, this SDK cookbook is based on Furiosa SDK version 2025.3.0
- [Install Prerequisites for Furiosa SDK](https://developer.furiosa.ai/latest/en/getting_started/prerequisites.html)
- [Navigate Furiosa SDK Documents](https://developer.furiosa.ai/latest/en/index.html)
  

## Beginner's guide 
This guide provides an introduction to using the Furiosa SDK for large language model (LLM) applications. The guide is intended for users new to the Furiosa SDK and covers the basic setup and usage required to get started. It includes:
- [Instruction for Generating LLM Inference Using Furiosa SDK](https://github.com/furiosa-ai/sdk-cookbook/blob/main/beginners-guide/use_generation.ipynb)
- [Steps for Implementing Tool Calling with Furiosa SDK to Build AI Agent](https://github.com/furiosa-ai/sdk-cookbook/blob/main/beginners-guide/use_tool_calling.ipynb)

## Usecase
| Name | Description | Framework / Integration                  | Use-case |
| --------- | --- | --- | --- |
| [Unit Test Generator](https://github.com/furiosa-ai/sdk-cookbook/tree/main/unit-test-generator) | LLM-based Code Explanation & Unit Test Generator | - | Text Generation |
| [Weekly News Reporter](https://github.com/furiosa-ai/sdk-cookbook/tree/main/weekly-news-reporter) | LLM-based Weekly News Retriever & Summarizer | LangGraph  | Multi Agent |
| [Simple RAG](https://github.com/furiosa-ai/sdk-cookbook/tree/main/simple-rag) | End-to-end Retrieval-Augmented Generation with custom documents | LangChain | RAG |
| [Financial AI Chatbot](https://github.com/furiosa-ai/sdk-cookbook/tree/main/finance-ai-chatbot) | Finance AI Chatbot with Query Routing | LangChain | Question Answering |
| [Coding Assistant](https://github.com/furiosa-ai/sdk-cookbook/tree/main/coding-assistant) | Open-Source Copilot for Code Completion & Assistance | Integration | Code Generation |
<!--| Agent with MCP adapter | Agent doing tool calling with MCP adapter | Integration | Agent | -->
<!--| Market Competitive Analysis | Multi-Agent doing market competitive analysis | BeeAI | Multi-agent | -->  

<!--  ## By Framework -->
<!-- | Framework | Name | Description                   | Tags | -->
<!--| --------- | --- | --- | --- | -->
<!--| LangGraph | [Weekly News Reporter](framework/langgraph/weekly_news_reporter) | Multi-agent example generate weekly news summary   | Multi-agent | -->
<!--| AutoGen | [CSV Chart Generation](csv-chart-generation) | Chart generation with chart type suggestion  | Multi-agent | -->


<!--## Framework Integrations -->
<!--| Framework | Description -->               
<!--| --------- | --- | -->
<!--| LangChain | | -->
<!--| AutoGen |  | -->
<!--| LiteLLM | | -->
<!--| SmolAgents | | -->
<!--| BeeAI | | -->


## How-to-Start
We recommend installing dependencies individually for each recipe in the cookbook. Every recipe has its own `README.md` and `requirements.txt`.
To get started with a recipe for building basic applications:

- Clone the `sdk-cookbook` repository.
- Choose a recipe and navigate to its folder.
- Set up a virtual environment.
- Install the necessary packages with `requirements.txt`.
- Follow the instructions in the `README.md` file.


## Support
Please note that the use-case examples in the Furiosa SDK CookBook are provided for guide purposes only and are not intended for production use. If you have questions or would like to discuss how to develop your own AI application using the Furiosa SDK, feel free to open a pull request or submit an issue. For broader discussions or support of Furiosa SDK, we encourage you to participate in the open forum linked below.
  - [FuriosaAI Forum](https://forums.furiosa.ai/)

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/furiosa-ai/sdk-cookbook/blob/main/LICENSE) file for further details.



