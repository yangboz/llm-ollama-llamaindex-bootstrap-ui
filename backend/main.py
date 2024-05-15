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


# ##@more：https://github.com/yangboz/local-rag-llamaindex/tree/master
# @app.post("/api/search", response_model=Response, status_code=200)
# def search_source(query: Query):

def get_search_source(query_str,similarity_top_k):

    my_query = Query(query_str,similarity_top_k)
    index = Depends(get_index)
    query_engine = index.as_query_engine(similarity_top_k=my_query.similarity_top_k, output=Response, response_mode="tree_summarize", verbose=True)
    response = query_engine.query(query.query_str + a)
    response_object = Response(
        search_result=str(response).strip(), source=[response.metadata[k]["file_path"] for k in response.metadata.keys()][0]
    )
    print("###search_response_object:",response_object)
    json_response_object = json.dumps(response_object)
    print("###json_response_object:",json_response_object)
    return response_object
    )
logging.info("app initialized.")
# record_timing(app, note="")

@r.post("")
async def chat(
            request: Request,
            # Note: To support clients sending a JSON object using content-type "text/plain",
            # we need to use Depends(json_to_model(_ChatData)) here
            data: _ChatData = Depends(json_to_model(_ChatData)),
            index: VectorStoreIndex = Depends(get_index),
            response_model=Response, status_code=200
            ):
# check preconditions and get last message
if len(data.messages) == 0:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No messages provided",
    )
lastMessage = data.messages.pop()
print("###lastMessage:",lastMessage)
if lastMessage.role != MessageRole.USER:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Last message must be from user",
    )
# convert messages coming from the request to type ChatMessage
messages = [
    ChatMessage(
        role=m.role,
        content=m.content,
        
    )
    for m in data.messages
]

# query chat engine with streaming enabled.
# chat_engine = index.as_query_engine(streaming=True, similarity_top_k=query.similarity_top_k, output=Response, response_mode="tree_sum")
# response = chat_engine.query(lastMessage.content)

# response = query_engine.query(query.query + a)
# response_object = Response(
#     search_result=str(response).strip(), source=[response.metadata[k]["file_path"] for k in response.metadata.keys()][0]
# )
# return response_object
# print("##chat_engine_response_object:",response_object)

# query chat engine with streaming enabled.
chat_engine = index.as_query_engine(streaming=True)
response = chat_engine.query(lastMessage.content)
print("###chat_respose:",response)
async def event_generator():
    for token in response.response_gen:
        # If client closes connection, stop sending events
        if await request.is_disconnected():
            break
        yield token
record_timing(request, note="tyllmwebchat")
# record_timing(note="tyllmwebchat")
return StreamingResponse(event_generator(), media_type="text/plain")
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)
