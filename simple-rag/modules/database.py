import os
import sys
from pathlib import Path
from functools import partial
import subprocess

from langchain_text_splitters import RecursiveCharacterTextSplitter
import psycopg
from pgvector.psycopg import register_vector

sys.path.append("..")
from modules.data import extract_sections
from modules.config import ROOT_DIR
from modules.embed import EmbedChunks

class StoreResults:
    def __call__(self, batch):
        with psycopg.connect(os.environ["DB_CONNECTION_STRING"]) as conn:
            register_vector(conn)
            with conn.cursor() as cur:
                for text, source, embedding in zip(batch["text"], batch["source"], batch["embeddings"]):
                    cur.execute("INSERT INTO document (text, source, embedding) VALUES (%s, %s, %s)", (text, source, embedding,),)
        return {}

def get_docs_dir(_config):
    dataset = _config["dataset"]
    efs_dir = f"./datasets/{dataset}"
    
    if dataset == "pytorch":
        html_dir = "pytorch.org/docs"
    else:
        raise ValueError(f"Unknown dataset: {dataset}")

    return Path(efs_dir, html_dir)

def create_db(_config):
    dataset = _config["dataset"]
    efs_dir = f"./datasets/{dataset}"
    chunk_size = _config["chunk_size"]
    chunk_overlap = _config["chunk_overlap"]
    embedding_model_name = _config["embedding_model_name"]
    create_DB_sh = f"{ROOT_DIR}/bash_scripts/create_DB.sh"
    # setup_pgvector_sh = f"{ROOT_DIR}/bash_scripts/setup-pgvector.sh"
    embedding_model_context_length = _config["embedding_model_context_length"]
    os.environ["MIGRATION_FP"] = f"./migrations/vector-{embedding_model_context_length}.sql"
    os.environ["SQL_DUMP_FP"] = f"{efs_dir}/sql_dumps/{embedding_model_name.split('/')[-1]}_{chunk_size}_{chunk_overlap}.sql"

    subprocess.run(f'bash {create_DB_sh}', shell=True, check=True)


def index_db(embedded_chunks, _config, batch_size=100):
    import numpy as np
    print(isinstance(embedded_chunks[0]['embeddings'], list))
    with psycopg.connect(os.environ["DB_CONNECTION_STRING"]) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            for i in range(len(embedded_chunks)):
                text = embedded_chunks[i]['text']
                source = embedded_chunks[i]['source']
                embedding = embedded_chunks[i]['embeddings']   
                cur.execute("INSERT INTO document (text, source, embedding) VALUES (%s, %s, %s)", (text, source, embedding,),)
    
    save_index_sh = "./bash_scripts/save_index.sh"
    subprocess.run(f'chmod +x {save_index_sh}', shell=True, check=True)



def get_embedded_chunks(_config, batch_size=100):
    docs_dir = get_docs_dir(_config)
    chunk_size = _config["chunk_size"]
    chunk_overlap = _config["chunk_overlap"]
    embedding_model_name = _config["embedding_model_name"]

    doc_paths = [path for path in docs_dir.rglob("*.html") if not path.is_dir()]
    print(f"{len(doc_paths)} documents")

    # Extract sections
    sections = []
    for path in doc_paths:
        sections.extend(extract_sections({"path": path}))

    print(f"{len(sections)} sections")

    # Scale chunking
    chunks = []
    for section in sections:
        chunks.extend(chunk_section(section, chunk_size=chunk_size, chunk_overlap=chunk_overlap))

    print(f"{len(chunks)} chunks")
    if chunks:
        print("Sample chunk:", chunks[0])

    # embed chunks 
    embedder = EmbedChunks(model_name=embedding_model_name)
    # for debug 
    chunks = chunks[:10]
    
    embedded_chunks = [embedder(chunk) for chunk in chunks]
    
    return embedded_chunks

def chunk_section(section, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len)
    chunks = text_splitter.create_documents(
        texts=[section["text"]], 
        metadatas=[{"source": section["source"]}])
    return [{"text": chunk.page_content, "source": chunk.metadata["source"]} for chunk in chunks]
