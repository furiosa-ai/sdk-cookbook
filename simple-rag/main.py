import os
import json

import sys

sys.path.append("..")
import warnings

warnings.filterwarnings("ignore")
from dotenv import load_dotenv

load_dotenv()

from modules import get_embedded_chunks, create_db, index_db, get_query_agent, get_data
from modules import DB_CONNECTION_STRING
from experiment_config import ex


@ex.automain
def main(_config):
    os.environ["DB_CONNECTION_STRING"] = DB_CONNECTION_STRING
    # Scrap data
    get_data(_config)

    # Get embedded chunks
    embedded_chunks = get_embedded_chunks(_config)

    # # Create and index DB
    create_db(_config)
    index_db(embedded_chunks, _config)

    # # Get query agent
    agent = get_query_agent(_config)

    # # Run RAG
    query = "How to import torch.nn?"
    result = agent(query=query, stream=False)
    print("==" * 20)
    print("question:", result["question"])
    print("answer:", result["answer"])

    # print(json.dumps(result, indent=2))
