from langchain_openai import ChatOpenAI
from langchain.chains.router import MultiRouteChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Dict, List, Any
from langchain.chains.base import Chain
from langchain.chains import LLMChain

import subprocess

def start_furiosa_llm_servers():
    server1 = subprocess.Popen(
        [
            "furiosa-llm",
            "serve",
            "furiosa-ai/Llama-3.1-8B-Instruct",
            "--host",
            "localhost",
            "--port",
            "8889",
            "--devices",
            "npu:1",
        ]
    )

    server2 = subprocess.Popen(
        [
            "furiosa-llm",
            "serve",
            "furiosa-ai/DeepSeek-R1-Distill-Llama-8B",
            "--enable-reasoning",
            "--reasoning-parser",
            "deepseek_r1",
            "--host",
            "localhost",
            "--port",
            "8888",
            "--devices",
            "npu:2",
        ]
    )
    return server1, server2



llm_easy = ChatOpenAI(
    base_url="http://localhost:8889/v1",  # llama-8b
    api_key="token-abc123",
    model="furiosa-ai/Llama-3.1-8B-Instruct"
)

llm_hard = ChatOpenAI(
    base_url="http://localhost:8888/v1",  # deepseek-8b
    api_key="token-abc456",
    model="furiosa-ai/DeepSeek-R1-Distill-Llama-8B"
)

# 1. Router Prompt
router_prompt_template = """
You are a helpful AI assistant that decides how to handle an incoming question by selecting a query augmentation strategy.

Choose one:
1. direct answer
2. add CoT
3. query rewrite
4. beyond ability

Return in JSON format:
{{
    "destination": "<one of: direct answer, add CoT, query rewrite, beyond ability>",
    "next_inputs": "<input question>",
}}

Question: What is 2 + 2?
Answer: {{"destination": "direct answer", "next_inputs": "What is 2 + 2?"}}

Question: {input}
"""


class RewriteThenAnswerChain(Chain):
    rewrite_chain: LLMChain
    answer_chain: LLMChain

    
    @property
    def input_keys(self) -> List[str]:
        return ["input"]
    
    @property
    def output_keys(self) -> List[str]:
        return ['text']

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        # Rewrite the question
        rewritten = self.rewrite_chain.invoke({"input": inputs["input"]})
        rewritten_text = rewritten['text']

        # Answer the rewritten question
        answer = self.answer_chain.invoke({"input": rewritten_text})
        return {"text": answer["text"]}

router_prompt = PromptTemplate.from_template(router_prompt_template,
                                             output_parser=RouterOutputParser())

router_chain = LLMRouterChain.from_llm(llm=llm_easy, prompt=router_prompt)

direct_prompt = PromptTemplate.from_template("Answer the question directly:\n\n{input}")

cot_prompt = PromptTemplate.from_template("Let's think step-by-step to answer the question:\n\n{input}")

rewrite_prompt = PromptTemplate.from_template("Rewrite this question to be more clear and precise:\n\n{input}")

direct_chain = LLMChain(llm=llm_easy, prompt=PromptTemplate.from_template(
    "Answer the question directly. Please do not include any thoughts. Just generate answer clearly:\n\n{input}"
))

cot_chain = LLMChain(llm=llm_easy, prompt=PromptTemplate.from_template(
    "Let's think step-by-step to answer the question:\n\n{input}"
))

rewrite_chain = LLMChain(llm=llm_easy, prompt=PromptTemplate.from_template(
    "Rewrite this question to be more clear and precise:\n\n{input}"
))

hard_chain = LLMChain(llm=llm_hard, prompt=PromptTemplate.from_template(
    "This is a difficult or expert-level question. Please try your best to answer:\n\n{input}"
))


if __name__ == "__main__":
    import time
    import json
    server1, server2 = start_furiosa_llm_servers()
    print("Furiosa-LLM servers started")
    time.sleep(100)

    rewrite_then_answer_chain = RewriteThenAnswerChain(rewrite_chain=rewrite_chain, 
                                            answer_chain=direct_chain) 
    strategy_chains = {
        "direct answer": direct_chain,
        "add CoT": cot_chain,
        "query rewrite": rewrite_then_answer_chain,
        "beyond ability": hard_chain, 
    }

    multi_chain = MultiRouteChain(
        router_chain=router_chain,
        destination_chains=strategy_chains,
        default_chain=hard_chain,
    )

    try:
        # What is the capital of France?

        # What is Prometheus used for in DevOps?

        # Does the equation 1 + 2 + 3 + 4 + 5 + ... = -1/12 actually make sense mathematically?

        # Prove or disprove: There are infinitely many twin primes.

        question = input("\n Please provide inputs: ")
        result = multi_chain.invoke({"input": question})

        # for logging purposes
        strategy_result = router_chain.invoke({"input": question})

        print(f"[Question] {strategy_result['input']}")
        print(f"[Strategy] {strategy_result['destination']}")
        print(f"\n Bot: {result['text']}")
    finally:
        server1.terminate()
        server2.terminate()
        server1.wait()
        server2.wait()
