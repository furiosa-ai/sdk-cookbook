import os
import sys
import numpy as np
import time

import psycopg
from pgvector.psycopg import register_vector

from furiosa_llm import LLM, SamplingParams
from transformers import AutoTokenizer

sys.path.append("..")

from modules.embed import get_embedding_model
from modules.utils import get_num_tokens, trim, get_client, get_lightllm_response


class QueryAgent:
    def __init__(
        self,
        embedding_model_name="text-embedding-ada-002",
        llm_name="furiosa-ai/Llama-3.1-8B-Instruct",
        temperature=0.0,
        _config=None,
    ):
        self.serving = _config["serving"]
        self.context_length = _config["llm_context_length"] - _config["max_new_tokens"]
        self.doc_context_length = int(0.7 * self.context_length)
        self.base_url = _config["base_url"]
        self.api_key = _config["api_key"]

        # Embedding model
        self.embedding_model_name = embedding_model_name
        self.embedding_model = get_embedding_model(
            embedding_model_name=embedding_model_name,
            model_kwargs={"device": "cuda"},
            encode_kwargs={"device": "cuda", "batch_size": 100},
        )

        # LLM
        self.llm_name = llm_name
        if self.serving == "api" or self.serving == "litellm":
            self.llm = llm_name
        elif self.serving == "local":
            self.llm = LLM.load_artifact(llm_name, devices="npu:3")

        self.tokenizer = AutoTokenizer.from_pretrained(llm_name)

        self.num_chunks = _config["num_chunks"]

        self.system_content = _config["system_content"]
        self.assistant_content = _config["assistant_content"]

        self.temperature = temperature
        self.max_new_tokens = _config["max_new_tokens"]

    def __call__(self, query, stream=True):
        # Get sources and context
        context_results = semantic_search(
            query=query, embedding_model=self.embedding_model, k=self.num_chunks
        )

        # Generate response
        context = [item["text"] for item in context_results]
        sources = [item["source"] for item in context_results]
        scores = [item["score"] for item in context_results]
        user_content = f"query: {query}, context: {context}"
        answer = generate_response(
            llm=self.llm,
            temperature=self.temperature,
            stream=stream,
            system_content=self.system_content,
            assistant_content=self.assistant_content,
            user_content=trim(user_content, self.doc_context_length),
            serving=self.serving,
            tokenizer=self.tokenizer,
            max_new_tokens=self.max_new_tokens,
            base_url=self.base_url,
            api_key=self.api_key,
        )

        result = {
            "question": query,
            "sources": sources,
            "context": context,
            "scores": scores,
            "answer": answer,
            "llm": self.llm_name,
            "embedding_model": self.embedding_model_name,
        }
        return result


def get_query_agent(_config):
    agent = QueryAgent(
        embedding_model_name=_config["embedding_model_name"],
        llm_name=_config["llm"],
        _config=_config,
    )

    return agent


def semantic_search(query, embedding_model, k):
    embedding = np.array(embedding_model.embed_query(query))
    with psycopg.connect(os.environ["DB_CONNECTION_STRING"]) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT *, (embedding <=> %s) AS similarity_score FROM document ORDER BY similarity_score LIMIT %s",
                (embedding, k),
            )
            rows = cur.fetchall()
            semantic_context = [
                {"id": row[0], "text": row[1], "source": row[2], "score": row[4]}
                for row in rows
            ]
    return semantic_context


def generate_response(
    llm,
    temperature=1.0,
    stream=True,
    system_content="",
    assistant_content="",
    user_content="",
    max_retries=1,
    retry_interval=60,
    serving="api",
    tokenizer=None,
    max_new_tokens=64,
    base_url="http://localhost:8888/v1",
    api_key="EMPTY",
):
    """Generate response from an LLM."""

    messages = [
        {"role": role, "content": content}
        for role, content in [
            ("system", system_content),
            ("assistant", assistant_content),
            ("user", user_content),
        ]
        if content
    ]

    if serving == "api":
        retry_count = 0
        client = get_client(llm=llm, base_url=base_url, api_key=api_key)
        while retry_count <= max_retries:
            try:
                chat_completion = client.chat.completions.create(
                    model=llm,
                    temperature=temperature,
                    stream=stream,
                    messages=messages,
                )
                return prepare_response(chat_completion, stream=stream)

            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(retry_interval)  # default is per-minute rate limits
                retry_count += 1
        return ""

    elif serving == "litellm":
        responses = get_lightllm_response(
            llm=llm,
            base_url=base_url,
            api_key=api_key,
            messages=messages,
        )
        return responses

    elif serving == "furiosa_llm":
        prompts = tokenizer.apply_chat_template(messages, tokenize=False)
        sampling_params = SamplingParams(
            temperature=temperature, max_tokens=max_new_tokens
        )
        outputs = llm.generate([prompts], sampling_params)
        return outputs[0].outputs[0].text


def response_stream(chat_completion):
    for chunk in chat_completion:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content


def prepare_response(chat_completion, stream):
    if stream:
        return response_stream(chat_completion)
    else:
        return chat_completion.choices[0].message.content
