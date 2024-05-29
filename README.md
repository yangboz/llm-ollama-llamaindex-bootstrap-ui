# Retrieval-Augmented Generation (RAG) Bootstrap Application UI

This is a [LlamaIndex](https://www.llamaindex.ai/) project bootstrapped with [`create-llama`](https://github.com/run-llama/LlamaIndexTS/tree/main/packages/create-llama) to act as a full stack UI to accompany **Retrieval-Augmented Generation (RAG) Bootstrap Application**, which can be found in its own repository at https://github.com/tyrell/llm-ollama-llamaindex-bootstrap 

[My blog post](https://www.tyrell.co/2023/12/weaving-path-to-relevance-leveraging.html) provides more context, motivation and thinking behind these projects.


![UI Screenshot](https://github.com/tyrell/llm-ollama-llamaindex-bootstrap-ui/blob/main/screenshots/ui-screenshot.png?raw=true)


The backend code of this application has been modified as below;

### weaviate
```
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.25.0
```
### ollama
```
curl -fsSL https://ollama.com/install.sh | sh
```

1. Loading the Vector Store Index created previously in the **Retrieval-Augmented Generation (RAG) Bootstrap Application** in response to user queries submitted through the frontend UI.



   -   Refer backend/app/utils/index.py and the code comments to understand the modifications.
2. Querying the index with streaming enabled 
   -   Refer backend/app/api/routers/chat.py and the code comments to understand the modifications.

## Running the full stack application

First, startup the backend as described in the [backend README](./backend/README.md).

Second, run the development server of the frontend as described in the [frontend README](./frontend/README.md).

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

##known issues

```
TypeError: SentenceTransformer.__init__() got an unexpected keyword argument 'trust_remote_code'
```
### workaround

1.
```
poetry install 
```
2.
```
uninstall llama-index
```
3.
```
pip install llama-index --upgrade --no-cache-dir --force-reinstall
```
# License

Apache 2.0

~ original Tyrell Perera 
