from furiosa_llm import LLM, SamplingParams
import asyncio
import subprocess
import time

# Load the Llama 3.1 8B Instruct model
llm = LLM.load_artifact("furiosa-ai/Llama-3.1-8B-Instruct-FP8", devices="npu:0")

# You can specify various parameters for text generation
sampling_params = SamplingParams(min_tokens=10, top_p=0.3, top_k=100)



# Prompt for the model
message = [{"role": "user", "content": "What is the capital of France?"}]
prompt = llm.tokenizer.apply_chat_template(message, tokenize=False)

# Generate text
response = llm.generate([prompt], sampling_params)

# Print the output of the model
print(response[0].outputs[0].text)


# ### 2. Multi batch inference 
messages = [[{"role": "user", "content": "What is the capital of France?"}],
            [{"role": "user", "content": "What is the capital of Germany?"}]]

prompts = [llm.tokenizer.apply_chat_template(message, tokenize=False) for message in messages]

# Generate text
responses = llm.generate(prompts, sampling_params)

# Print the output of the model
outputs = [responses[i].outputs[0].text.split("assistant\n\n")[-1] for i in range(len(responses))]
for i, output in enumerate(outputs):
    print(f"Batch {i+1}")
    print(f"Question {i + 1}: {messages[i][0]['content']}")
    print(f"Response {i + 1}: {output}")
    print("====================================================")



 
async def async_single_batch_inference():
    # Prompt for the model
    message = [{"role": "user", "content": "What is the capital of France?"}]
    prompt = llm.tokenizer.apply_chat_template(message, tokenize=False)

    # Generate text and print each token at a time
    async for output_txt in llm.stream_generate(prompt, sampling_params):
        print(output_txt, end="", flush=True)

asyncio.run(async_single_batch_inference())


