from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
import subprocess
import time
from finance_chatbot import FinanceChatbot

app = FastAPI()
chatbot = FinanceChatbot()


class QueryRequest(BaseModel):
    question: str
    user_id: str


@app.post("/chat")
async def chat(request: QueryRequest):
    # try:
    response = await chatbot.get_response(request.question, request.user_id)

    if hasattr(response, "content"):
        response_text = response.content
    else:
        response_text = str(response)

    return {
        "user_id": request.user_id,
        "question": request.question,
        "response": response_text,
    }
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


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
            "npu:2",
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
            "npu:3",
        ]
    )
    return server1, server2


if __name__ == "__main__":

    server1, server2 = start_furiosa_llm_servers()
    time.sleep(100)
    print("furiosa-llm servers started")
    try:
        client = TestClient(app)

        payload = {
            "question": "How do you see the US interest and stock market outlook?",
            "user_id": "user_123",
        }

        response = client.post("/chat", json=payload)

        if response.status_code == 200:
            print("✅ success:")
            response = response.json()
            print("question", response["question"])
            print("response", response["response"])

        else:
            print("❌ fail:", response.status_code, response.text)

    finally:
        server1.terminate()
        server2.terminate()
        server1.wait()
        server2.wait()
