from sacred import Experiment

ex = Experiment("METER", save_git_info=False)


@ex.capture
def capture_config(_config):
    return _config


@ex.config
def config():
    dataset = "pytorch"

    # serving
    serving = "litellm"  # api, local, litellm

    base_url = "http://localhost:8888/v1"  # for api serving
    api_key = "EMPTY"  # for api serving

    # model
    embedding_model_name = "text-embedding-ada-002"
    embedding_model_context_length = 1536
    llm = "furiosa-ai/Llama-3.1-8B-Instruct"
    llm_context_length = 12288
    # retreival
    num_chunks = 5
    chunk_size = 300
    chunk_overlap = 50

    # generation
    system_content = "Answer the query using the context provided. Be succinct."
    assistant_content = ""

    max_new_tokens = 1024  # for output (max_new_tokens of transformers)
    temperature = 1


@ex.named_config
def PytorchDataset():
    dataset = "pytorch"
    num_chunks = 5
    chunk_overlap = 0
    context_length_custom = 512
