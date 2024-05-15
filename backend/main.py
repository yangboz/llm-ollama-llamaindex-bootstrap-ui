from dotenv import load_dotenv
load_dotenv()

import logging
import os
import uvicorn
from pydantic import BaseModel,Field


from typing import  Optional,List


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
## api time logging , @see:https://fastapi-utils.davidmontague.xyz/user-guide/timing-middleware/
import logging
from fastapi_utils.timing import add_timing_middleware, record_timing

from llama_index.core.llms import ChatMessage, MessageRole


app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set


if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")

# app.include_router(chat_router, prefix="/api/chat")
# app.include_router(search_router, prefix="/api/search")


# search_router = r = APIRouter()

app = FastAPI()


class _Message(BaseModel):
    role: MessageRole
    content: str
    


class _ChatData(BaseModel):
    messages: list[_Message]


class Query(BaseModel):
    query: str
    similarity_top_k: Optional[int] = Field(default=1, ge=1, le=5)


class Response(BaseModel):
    search_result: str 
    source: str



 def qdrant_index(self):
        client = qdrant_client.QdrantClient(url=self.config["qdrant_url"])
        qdrant_vector_store = QdrantVectorStore(
            client=client, collection_name=self.config['collection_name']
        )
        # service_context = ServiceContext.from_defaults(
        #     llm=self.llm, embed_model="local:BAAI/bge-small-en-v1.5"
        # )

        service_context = ServiceContext.from_defaults(
            llm=self.llm, embed_model=self.load_embedder(), chunk_size=self.config["chunk_size"]
        )

        index = VectorStoreIndex.from_vector_store(
            vector_store=qdrant_vector_store, service_context=service_context
        )
        return index

##@more：https://github.com/yangboz/local-rag-llamaindex/tree/master
@app.post("/api/search", response_model=Response, status_code=200)
def search(query: Query):

    query_engine = self.qdrant_index.as_query_engine(similarity_top_k=query.similarity_top_k, output=Response, response_mode="tree_summarize", verbose=True)
    response = query_engine.query(query.query + a)
    response_object = Response(
        search_result=str(response).strip(), source=[response.metadata[k]["file_path"] for k in response.metadata.keys()][0]
    )
    print("###search_response_object:",response_object)
    json_response_object = json.dumps(response_object)
    print("###json_response_object:",json_response_object)
    return response_object


logging.info("app initialized.")
# record_timing(app, note="")



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
