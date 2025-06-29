# code from langgraph example: https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/ainsight_langgraph.ipynb
# Changes:
#   The connection address for ChatOpenAI has benn updated to an RNGD-based OpenAI-comptaible server.
#   The Tavily API call results are now stored, allowing execution without an API key.

import os
import json
import time
from datetime import datetime
import re
import subprocess
import openai

model = 'Qwen2.5-Coder-32B-Instruct'

def get_sample_code():
    print('Using Sample calculator code based on Recursive descent parser')
    return open('examples/calculator.py').read()

def generate_explanation(code):
    system_prompt_expl = (
        "You are a helpful assistant. Given Python code, provide a concise explanation "
        "labeled '## Explanation'."
    )
    expl_messages = [
        {"role": "system", "content": system_prompt_expl},
        {"role": "user", "content": f"Here is the Python code:\n\n{code}"},
    ]
    resp_expl = openai.chat.completions.create(
        model=model,
        messages=expl_messages,
    )
    expl_raw = resp_expl.choices[0].message.content
    if "</think>" in expl_raw:
        expl_raw = expl_raw.split("</think>", 1)[1]
    if expl_raw.lower().startswith("## explanation"):
        expl_text = "\n".join(expl_raw.splitlines()[1:]).strip()
    else:
        expl_text = expl_raw.strip()
    return expl_text

def generate_unittest(code, explanation):
    system_prompt_tests = (
        "You are a helpful assistant. Given Python code and its explanation, "
        "provide Python unittests labeled '## Unittests' using the unittest framework."
    )
    test_messages = [
        {"role": "system", "content": system_prompt_tests},
        {"role": "user", "content": f"Here is the Python code:\n\n{code}"},
        {"role": "user", "content": f"## Explanation\n{explanation}"},
    ]
    resp_tests = openai.chat.completions.create(
        model=model,
        messages=test_messages,
    )
    tests_raw = resp_tests.choices[0].message.content
    if "</think>" in tests_raw:
        tests_raw = tests_raw.split("</think>", 1)[1]
    parts = re.split(r"## Unittests", tests_raw, maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else tests_raw.strip()

def start_furiosa_llm_servers():
    server = subprocess.Popen(
        [
            "furiosa-llm",
            "serve",
            "furiosa-ai/Qwen2.5-Coder-32B-Instruct",
            "--host",
            "localhost",
            "--port",
            "8000",
            "--devices",
            "npu:2,npu:3",
        ]
    )
    return server

if __name__ == "__main__":

    server = start_furiosa_llm_servers()
    time.sleep(100)
    openai.base_url = 'http://localhost:8000/v1/'
    openai.api_key = 'EMPTY'
    try:
        # Display results
        print("\n=== Unittest Generation ===\n")
        print("\n=== LLM-based Code Explanation & Unittest Generator ===\n")
        code = get_sample_code()
        explanation = generate_explanation(code)
        print(explanation)
        unittests = generate_unittest(code, explanation)
        print(unittests)
    finally:
        server.terminate()  # Clean up server after execution
        server.wait()
