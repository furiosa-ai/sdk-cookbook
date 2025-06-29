# LLM-based Code Explanation & Unittest Generator

Interactive demo application built with Streamlit and the OpenAI API. Upload Python files, generate concise explanations, and automatically produce `unittest` test cases. Iteratively refine tests with custom prompts.

## Features

- Upload one or more Python `.py` files
- Generate concise code explanations
- Produce Python `unittest` tests for the uploaded code
- Copy to clipboard or download generated tests
- Iteratively refine tests using additional prompts

## Installation

### Requirements

- FuriosaSDK 2025.3.0
- RNGD server or Endpoint API

### Steps

```bash
# Clone the repository (replace URL with your fork)
git clone https://github.com/furiosa-ai/sdk-cookbook.git
cd unit-test-generator

# Install dependencies
pip install -r requirements.txt
```

## Configuration

- LLM : [furiosa-ai/Qwen2.5-Coder-32B-Instruct](https://huggingface.co/furiosa-ai/Qwen2.5-Coder-32B-Instruct)

## Usage

```
python app.py
```

Or Launch the Streamlit app with launching RNGD server:

```
furiosa-llm serve furiosa-ai/Qwen2.5-Coder-32B-Instruct \
    --host localhost --port 8000 --devices npu:2,npu:3
```

```bash
streamlit run web_app.py
```

In the sidebar, enter your API key (and any optional settings). Then upload Python `.py` files to generate explanations and tests. Use **Generate Explanation & Tests** for a one-step process or generate explanation and tests separately. Refine tests by entering additional prompts and clicking **Apply Fix**.

## Examples

The `examples/` folder contains sample modules to try out the demo:

- `examples/calculator.py`: recursive-descent arithmetic parser
- `examples/polynomial.py`: polynomial arithmetic and evaluation

## Project Structure

```
.
├── app.py            # Streamlit application
├── examples/         # Sample Python modules
│   ├── calculator.py
│   └── polynomial.py
├── README.md         # Project documentation
├── requirements.txt  # Python dependencies
└── pyproject.toml    # Project metadata
```

