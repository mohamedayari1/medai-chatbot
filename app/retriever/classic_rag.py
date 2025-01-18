import os
from app.core.settings import settings
from app.retriever.base import BaseRetriever

from app.models.db_models import Conversation, QnA
from app.utils.token_management import num_tokens_from_string
# from app.retriever.quick_and_dirty_rag import VectorRetriever
from app.utils.logging import get_logger
from app.schemas.answer import AnswerRequest, AnswerResponse
from app.schemas.search import SearchRequest, SearchResponse


from app.llm.openai import AzureOpenAILLM

import httpx
import asyncio

async def get_rag_response(prompt: str):
    async with httpx.AsyncClient() as client:
        try:
            # Define the request payload
            payload = {"prompt": prompt}

            # Send a POST request to the /rag endpoint
            response = await client.post("http://localhost:8001/rag", json=payload)

            # Raise an error for bad responses
            response.raise_for_status()

            # Parse the response JSON
            retriever_response = response.json()

            # Unpack the response into sources and text_to_highlight
            sources = retriever_response["sources"]
            text_to_highlight = retriever_response["text_to_highlight"]

            return sources, text_to_highlight

        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            return None, None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None, None



logger = get_logger(__name__)


from motor.motor_asyncio import AsyncIOMotorClient
# MongoDB setup
MONGO_URI = "mongodb+srv://zoldyck:zoldyck@cluster0.kjantw5.mongodb.net/"
DATABASE_NAME = "test"
COLLECTION_NAME = "test_conversations"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

async def ensure_collection_exists():
    if COLLECTION_NAME not in await db.list_collection_names():
        await db.create_collection(COLLECTION_NAME)




llm = AzureOpenAILLM()


conversation_id="dev-123456789"

async def get_conversation(userId):
    # return await collection.find_one({"userId": userId})
    return await collection.find_one({"conversation_id": conversation_id})




async def upsert_conversation(conversation):
    await collection.update_one(
        # {"userId": conversation.userId},
        {"userId": conversation_id},
        {"$set": conversation.dict()},
        upsert=True
    )

class ClassicRAG(BaseRetriever):

    def __init__(
        self,
        question,
        # source,
        # chat_history,
        prompt,
        chunks=2,
        token_limit=1500,
        # gpt_model="docsgpt",
        # user_api_key=None,
    ):
        self.question = question
        # self.vectorstore = source["active_docs"] if "active_docs" in source else None
        # self.chat_history = chat_history
        self.prompt = prompt
        self.chunks = chunks
        # self.gpt_model = gpt_model
        # self.token_limit = (
        #     token_limit
        #     if token_limit
        #     < settings.MODEL_TOKEN_LIMITS.get(
        #         self.gpt_model, settings.DEFAULT_MAX_HISTORY
        #     )
        #     else settings.MODEL_TOKEN_LIMITS.get(
        #         self.gpt_model, settings.DEFAULT_MAX_HISTORY
        #     )
        # )
        self.token_limit = 1500
        # self.user_api_key = user_api_key

    # async def _get_data(self, query: str):
    #     if self.chunks == 0:
    #         docs = []
    #     else:
    #         # docsearch = VectorCreator.create_vectorstore(
    #         #     settings.VECTOR_STORE, self.vectorstore, settings.EMBEDDINGS_KEY
    #         # )
    #         retriever = VectorRetriever(query=query)

    #         docs_temp = retriever.retrieve_top_k(9)
    #         docs = [
    #             {
    #                 "title": doc.payload.get("platform", "Untitled").split("/")[-1],
    #                 "text": doc.payload.get("content", ""),
    #                 "source": doc.payload.get("link", "local"),
    #             }
    #             for doc in docs_temp
    #         ]
    #         return docs

    async def gen(self, userId: str=conversation_id):
        # docs = await self._get_data()
        # docs = await self._get_data(query=self.question)

        # # join all page_content together with a newline
        # docs_together = "\n".join([doc["text"] for doc in docs])
        # text_to_highlight = [doc["text"] for doc in docs]
        # sources = [doc["source"] for doc in docs]
        
          # Example usage
        sources, text_to_highlight = await get_rag_response(self.question)
        docs_together = "\n".join(text_to_highlight)
        p_chat_combine = self.prompt.replace("{summaries}", docs_together)
        messages_combine = [{"role": "system", "content": p_chat_combine}]
        

        
        conversation_data = await get_conversation(userId)

        if conversation_data:
            conversation = Conversation(**conversation_data)
            qna_list = conversation.qna_list
            tokens_current_history = 0

            for qna_item in qna_list:
                # prompt = qna_item.get("prompt")
                # response = qna_item.get("response")
                prompt = qna_item.prompt  # Access attribute directly
                response = qna_item.response  # Access attribute directly
                if not prompt or not response:
                    continue

                tokens_for_pair = num_tokens_from_string(prompt) + num_tokens_from_string(response)
                if tokens_current_history + tokens_for_pair < self.token_limit:
                    tokens_current_history += tokens_for_pair
                    messages_combine.extend([
                        {"role": "user", "content": prompt},
                        {"role": "system", "content": response},
                    ])
        else:
            # conversation = Conversation(userId=userId)
            conversation = Conversation(userId=conversation_id)
        messages_combine.append({"role": "user", "content": self.question})
        logger.info(f"Combined messages being sent to OpenAI: {messages_combine}")

        answer = llm._raw_gen(model="chat", messages=messages_combine)
    # Return hardcoded response for development
        response = AnswerResponse(
            answer=answer,
            sources=[
                {
                    "source": sources[1],
                    "text": "".join(text_to_highlight),
                    "metadata": {"page": 1}
                }
            ],
            conversation_id=conversation_id
        )
        
        question_and_answer = QnA(prompt=self.question, response=answer)
        conversation.qna_list.append(question_and_answer)

        await upsert_conversation(conversation)


        return response