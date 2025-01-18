import asyncio
import datetime
import json
import logging
import os
import sys
import traceback
from typing import AsyncGenerator

from app.retriever.classic_rag import ClassicRAG

# from bson.dbref import DBRef
# from bson.objectid import ObjectId

# from pymongo import MongoClient

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse


# from app.core.config import settings
# from app.core.mongo_db import MongoDB
# from app.llm.llm_creator import LLMCreator
# from app.retriever.retriever_creator import RetrieverCreator

# from app.schemas.stream import (
#     StreamRequest,
#     StreamResponse,
#     StreamSourceEvent,
#     StreamAnswerEvent,
#     StreamIdEvent,
#     StreamErrorEvent,
#     StreamEndEvent
# # )

from app.schemas.answer import AnswerRequest, AnswerResponse
# from app.schemas.search import SearchRequest, SearchResponse
from app.llm.openai import AzureOpenAILLM
llm = AzureOpenAILLM()

router = APIRouter()

logger = logging.getLogger(__name__)



# Determine the directory of the current script and construct the path to prompts
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS_DIR = os.path.join(CURRENT_DIR, "../prompts")

# Load prompts
try:
    with open(os.path.join(PROMPTS_DIR, "chat_combine_default.txt"), "r") as file:
        CHAT_COMBINE = file.read()
        print(CHAT_COMBINE)
except FileNotFoundError as e:
    logger.error(f"Prompt file not found: {e}")
    raise FileNotFoundError("Prompt file  is missing. Please ensure it is in the 'prompts' directory.")
# mongo = MongoDB.get_client()
# db = mongo["docsgpt"]
# conversations_collection = db["conversations"]
# sources_collection = db["sources"]
# prompts_collection = db["prompts"]
# api_key_collection = db["api_keys"]
# user_logs_collection = db["user_logs"]

# gpt_model = ""
# if settings.LLM_NAME == "openai":
#     gpt_model = "gpt-3.5-turbo"
# elif settings.LLM_NAME == "anthropic":
#     gpt_model = "claude-2"
# elif settings.LLM_NAME == "groq":
#     gpt_model = "llama3-8b-8192"

# if settings.MODEL_NAME:
#     gpt_model = settings.MODEL_NAME

# # Load prompts
# current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# with open(os.path.join(current_dir, "prompts", "chat_combine_default.txt"), "r") as f:
#     chat_combine_template = f.read()

# with open(os.path.join(current_dir, "prompts", "chat_reduce_prompt.txt"), "r") as f:
#     chat_reduce_template = f.read()

# with open(os.path.join(current_dir, "prompts", "chat_combine_creative.txt"), "r") as f:
#     chat_combine_creative = f.read()

# with open(os.path.join(current_dir, "prompts", "chat_combine_strict.txt"), "r") as f:
#     chat_combine_strict = f.read()

# api_key_set = settings.API_KEY is not None
# embeddings_key_set = settings.EMBEDDINGS_KEY is not None

async def async_generate(chain, question, chat_history):
    pass
    # result = await chain.arun({"question": question, "chat_history": chat_history})
    # return result

def run_async_chain(chain, question, chat_history):
    pass
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # result = {}
    # try:
    #     answer = loop.run_until_complete(async_generate(chain, question, chat_history))
    # finally:
    #     loop.close()
    # result["answer"] = answer
    # return result

def get_data_from_api_key(api_key: str):
    pass
    # data = api_key_collection.find_one({"key": api_key})
    # if data is None:
    #     raise HTTPException(status_code=401, detail="Invalid API Key, please generate new key")

    # if "retriever" not in data:
    #     data["retriever"] = None

    # if "source" in data and isinstance(data["source"], DBRef):
    #     source_doc = db.dereference(data["source"])
    #     data["source"] = str(source_doc["_id"])
    #     if "retriever" in source_doc:
    #         data["retriever"] = source_doc["retriever"]
    # else:
    #     data["source"] = {}
    # return data

def get_retriever(source_id: str):
    pass
    # doc = sources_collection.find_one({"_id": ObjectId(source_id)})
    # if doc is None:
    #     raise HTTPException(status_code=404, detail="Source document does not exist")
    # retriever_name = None if "retriever" not in doc else doc["retriever"]
    # return retriever_name

def get_prompt(prompt_id: str):
    pass 
    # if prompt_id == "default":
    #     prompt = chat_combine_template
    # elif prompt_id == "creative":
    #     prompt = chat_combine_creative
    # elif prompt_id == "strict":
    #     prompt = chat_combine_strict
    # else:
    #     prompt = prompts_collection.find_one({"_id": ObjectId(prompt_id)})["content"]
    # return prompt

def save_conversation(conversation_id, question, response, source_log_docs, llm):
    pass
    # if conversation_id is not None and conversation_id != "None":
    #     conversations_collection.update_one(
    #         {"_id": ObjectId(conversation_id)},
    #         {
    #             "$push": {
    #                 "queries": {
    #                     "prompt": question,
    #                     "response": response,
    #                     "sources": source_log_docs,
    #                 }
    #             }
    #         },
    #     )
    #     return conversation_id
    # else:
    #     messages_summary = [
    #         {
    #             "role": "assistant",
    #             "content": "Summarise following conversation in no more than 3 "
    #             "words, respond ONLY with the summary, use the same "
    #             "language as the system \n\nUser: "
    #             + question
    #             + "\n\n"
    #             + "AI: "
    #             + response,
    #         },
    #         {
    #             "role": "user",
    #             "content": "Summarise following conversation in no more than 3 words, "
    #             "respond ONLY with the summary, use the same language as the "
    #             "system",
    #         },
    #     ]

    #     completion = llm.gen(model=gpt_model, messages=messages_summary, max_tokens=30)
    #     conversation_id = conversations_collection.insert_one(
    #         {
    #             "user": "local",
    #             "date": datetime.datetime.utcnow(),
    #             "name": completion,
    #             "queries": [
    #                 {
    #                     "prompt": question,
    #                     "response": response,
    #                     "sources": source_log_docs,
    #                 }
    #             ],
    #         }
    #     ).inserted_id
    #     return str(conversation_id)

async def stream_generator(
    question: str,
    retriever,
    conversation_id: str | None,
    user_api_key: str | None,
    isNoneDoc: bool = False
) -> AsyncGenerator[str, None]:
    pass
    # try:
    #     response_full = ""
    #     source_log_docs = []
    #     answer = retriever.gen()
    #     sources = retriever.search()
        
    #     if len(sources) > 0:
    #         for source in sources:
    #             if "text" in source:
    #                 source["text"] = source["text"][:100].strip() + "..."
    #         yield json.dumps(StreamSourceEvent(type="source", source=sources).dict()) + "\n"

    #     for line in answer:
    #         if "answer" in line:
    #             response_full += str(line["answer"])
    #             yield json.dumps(StreamAnswerEvent(type="answer", answer=line["answer"]).dict()) + "\n"
    #         elif "source" in line:
    #             source_log_docs.append(line["source"])

    #     if isNoneDoc:
    #         for doc in source_log_docs:
    #             doc["source"] = "None"

    #     llm = LLMCreator.create_llm(
    #         settings.LLM_NAME, api_key=settings.API_KEY, user_api_key=user_api_key
    #     )
        
    #     if user_api_key is None:
    #         conversation_id = save_conversation(
    #             conversation_id, question, response_full, source_log_docs, llm
    #         )
    #         yield json.dumps(StreamIdEvent(type="id", id=str(conversation_id)).dict()) + "\n"

    #     retriever_params = retriever.get_params()
    #     user_logs_collection.insert_one(
    #         {
    #             "action": "stream_answer",
    #             "level": "info",
    #             "user": "local",
    #             "api_key": user_api_key,
    #             "question": question,
    #             "response": response_full,
    #             "sources": source_log_docs,
    #             "retriever_params": retriever_params,
    #             "timestamp": datetime.datetime.now(datetime.timezone.utc),
    #         }
    #     )
    #     yield json.dumps(StreamEndEvent(type="end").dict()) + "\n"

    # except Exception as e:
    #     logger.error(f"Error in stream: {str(e)}", exc_info=True)
    #     yield json.dumps(
    #         StreamErrorEvent(
    #             type="error",
    #             error="Please try again later. We apologize for any inconvenience.",
    #             error_exception=str(e)
    #         ).dict()
    #     ) + "\n"




@router.post("/api/answer", response_model=AnswerResponse)
async def answer_endpoint(request: AnswerRequest):
    # Validate request by accepting it with the AnswerRequest model
    # All validation is handled automatically by Pydantic
    

    try:
        rag_agent = ClassicRAG(
            question=request.question,
            prompt=CHAT_COMBINE
        )
        # Await the async gen() method
        response = await rag_agent.gen()

        
        # Return a properly structured AnswerResponse
        return response
    except Exception as e:
        # Log the full error with traceback
        traceback.print_exc()
        # Re-raise the exception to let FastAPI handle it
        raise HTTPException(status_code=500, detail=str(e))


    
    # combined_messages = [{"role": "system", "content": "You are a helpful AI assistant, LawGPT, designed to offer detailed and informative responses. You are a legal expert and can answer questions about the law."}]
    # combined_messages.append({"role": "user", "content": request.question})

    
    # answer = llm._raw_gen(model="chat", messages=combined_messages)
    # # Return hardcoded response for development
    # return AnswerResponse(
    #     answer=answer,
    #     sources=[
    #         {
    #             "source": "example.md",
    #             "text": "This is a sample source text that would normally come from the retriever.",
    #             "metadata": {"page": 1}
    #         }
    #     ],
    #     conversation_id="dev-123456789"
    # )
    
    
    
    

    # Original implementation commented out:
    # try:
    #     question = request.question
    #     history = request.history
    #     conversation_id = request.conversation_id
    #     prompt_id = request.prompt_id
    #     chunks = request.chunks
    #     token_limit = request.token_limit or settings.DEFAULT_MAX_HISTORY
    #     retriever_name = request.retriever
    #
    #     if request.api_key:
    #         data_key = get_data_from_api_key(request.api_key)
    #         chunks = int(data_key.get("chunks", 2))
    #         prompt_id = data_key.get("prompt_id", "default")
    #         source = {"active_docs": data_key.get("source")}
    #         retriever_name = data_key.get("retriever", retriever_name)
    #         user_api_key = request.api_key
    #     elif request.active_docs:
    #         source = {"active_docs": request.active_docs}
    #         retriever_name = get_retriever(request.active_docs) or retriever_name
    #         user_api_key = None
    #     else:
    #         source = {}
    #         user_api_key = None
    #
    #     logger.info(
    #         f"/api/answer - request_data: {request.dict()}, source: {source}",
    #         extra={"data": json.dumps({"request_data": request.dict(), "source": source})}
    #     )
    #
    #     prompt = get_prompt(prompt_id)
    #
    #     retriever = RetrieverCreator.create_retriever(
    #         retriever_name,
    #         question=question,
    #         source=source,
    #         chat_history=history,
    #         prompt=prompt,
    #         chunks=chunks,
    #         token_limit=token_limit,
    #         gpt_model=gpt_model,
    #         user_api_key=user_api_key,
    #     )
    #
    #     source_log_docs = []
    #     response_full = ""
    #     for line in retriever.gen():
    #         if "source" in line:
    #             source_log_docs.append(line["source"])
    #         elif "answer" in line:
    #             response_full += line["answer"]
    #
    #     if request.isNoneDoc:
    #         for doc in source_log_docs:
    #             doc["source"] = "None"
    #
    #     llm = LLMCreator.create_llm(
    #         settings.LLM_NAME, api_key=settings.API_KEY, user_api_key=user_api_key
    #     )
    #
    #     conversation_id = save_conversation(
    #         conversation_id, question, response_full, source_log_docs, llm
    #     )
    #
    #     retriever_params = retriever.get_params()
    #     user_logs_collection.insert_one(
    #         {
    #             "action": "api_answer",
    #             "level": "info",
    #             "user": "local",
    #             "api_key": user_api_key,
    #             "question": question,
    #             "response": response_full,
    #             "sources": source_log_docs,
    #             "retriever_params": retriever_params,
    #             "timestamp": datetime.datetime.now(datetime.timezone.utc),
    #         }
    #     )
    #
    #     return AnswerResponse(
    #         answer=response_full,
    #         sources=source_log_docs,
    #         conversation_id=str(conversation_id)
    #     )
    #
    # except Exception as e:
    #     logger.error(
    #         f"/api/answer - error: {str(e)} - traceback: {traceback.format_exc()}",
    #         extra={"error": str(e), "traceback": traceback.format_exc()},
    #     )
    #     raise HTTPException(status_code=500, detail=str(e))








# @router.post("/stream")
# async def stream_endpoint(request: StreamRequest) -> StreamingResponse:
#     try:
#         question = request.question
#         history = request.history
#         conversation_id = request.conversation_id
#         prompt_id = request.prompt_id
#         chunks = request.chunks
#         token_limit = request.token_limit or settings.DEFAULT_MAX_HISTORY
#         retriever_name = request.retriever

#         if request.api_key:
#             data_key = get_data_from_api_key(request.api_key)
#             chunks = int(data_key.get("chunks", 2))
#             prompt_id = data_key.get("prompt_id", "default")
#             source = {"active_docs": data_key.get("source")}
#             retriever_name = data_key.get("retriever", retriever_name)
#             user_api_key = request.api_key
#         elif request.active_docs:
#             source = {"active_docs": request.active_docs}
#             retriever_name = get_retriever(request.active_docs) or retriever_name
#             user_api_key = None
#         else:
#             source = {}
#             user_api_key = None

#         logger.info(
#             f"/stream - request_data: {request.dict()}, source: {source}",
#             extra={"data": json.dumps({"request_data": request.dict(), "source": source})}
#         )

#         prompt = get_prompt(prompt_id)
#         if request.isNoneDoc:
#             chunks = 0

#         retriever = RetrieverCreator.create_retriever(
#             retriever_name,
#             question=question,
#             source=source,
#             chat_history=history,
#             prompt=prompt,
#             chunks=chunks,
#             token_limit=token_limit,
#             gpt_model=gpt_model,
#             user_api_key=user_api_key,
#         )

#         return StreamingResponse(
#             stream_generator(
#                 question=question,
#                 retriever=retriever,
#                 conversation_id=conversation_id,
#                 user_api_key=user_api_key,
#                 isNoneDoc=request.isNoneDoc,
#             ),
#             media_type="text/event-stream"
#         )

#     except Exception as e:
#         logger.error(
#             f"/stream - error: {str(e)} - traceback: {traceback.format_exc()}",
#             extra={"error": str(e), "traceback": traceback.format_exc()},
#         )
#         if len(e.args) >= 2:
#             raise HTTPException(status_code=e.args[1], detail=e.args[0])
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/api/search", response_model=SearchResponse)
# async def search_endpoint(request: SearchRequest):
#     try:
#         question = request.question
#         chunks = request.chunks
#         token_limit = request.token_limit or settings.DEFAULT_MAX_HISTORY
#         retriever_name = request.retriever

#         if request.api_key:
#             data_key = get_data_from_api_key(request.api_key)
#             chunks = int(data_key.get("chunks", 2))
#             source = {"active_docs": data_key.get("source")}
#             user_api_key = request.api_key
#         elif request.active_docs:
#             source = {"active_docs": request.active_docs}
#             user_api_key = None
#         else:
#             source = {}
#             user_api_key = None

#         logger.info(
#             f"/api/search - request_data: {request.dict()}, source: {source}",
#             extra={"data": json.dumps({"request_data": request.dict(), "source": source})}
#         )

#         retriever = RetrieverCreator.create_retriever(
#             retriever_name,
#             question=question,
#             source=source,
#             chat_history=[],
#             prompt="default",
#             chunks=chunks,
#             token_limit=token_limit,
#             gpt_model=gpt_model,
#             user_api_key=user_api_key,
#         )

#         docs = retriever.search()
#         retriever_params = retriever.get_params()

#         user_logs_collection.insert_one(
#             {
#                 "action": "api_search",
#                 "level": "info",
#                 "user": "local",
#                 "api_key": user_api_key,
#                 "question": question,
#                 "sources": docs,
#                 "retriever_params": retriever_params,
#                 "timestamp": datetime.datetime.now(datetime.timezone.utc),
#             }
#         )

#         if request.isNoneDoc:
#             for doc in docs:
#                 doc["source"] = "None"

#         return SearchResponse(results=docs)

#     except Exception as e:
#         logger.error(
#             f"/api/search - error: {str(e)} - traceback: {traceback.format_exc()}",
#             extra={"error": str(e), "traceback": traceback.format_exc()},
#         )
#         raise HTTPException(status_code=500, detail=str(e))