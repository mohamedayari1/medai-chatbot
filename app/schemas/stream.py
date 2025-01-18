# schemas/stream.py
from base import Source, ChatHistory
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, Field



class StreamRequest(BaseModel):
    question: str = Field(..., description="Question to be asked")
    history: Optional[List[ChatHistory]] = Field(default_factory=list, description="Chat history")
    conversation_id: Optional[str] = None
    prompt_id: str = Field(default="default", description="Prompt ID to be used")
    chunks: int = Field(default=2, ge=0, description="Number of chunks to process")
    token_limit: Optional[int] = Field(None, gt=0, description="Maximum token limit")
    retriever: str = Field(default="classic", description="Type of retriever to use")
    api_key: Optional[str] = None
    active_docs: Optional[str] = None
    isNoneDoc: bool = Field(default=False, description="Flag for no document usage")

    class Config:
        schema_extra = {
            "example": {
                "question": "How do I implement authentication?",
                "history": [],
                "prompt_id": "default",
                "chunks": 2
            }
        }

class StreamSourceEvent(BaseModel):
    type: Literal["source"]
    source: List[Source]

class StreamAnswerEvent(BaseModel):
    type: Literal["answer"]
    answer: str

class StreamIdEvent(BaseModel):
    type: Literal["id"]
    id: str

class StreamErrorEvent(BaseModel):
    type: Literal["error"]
    error: str
    error_exception: Optional[str] = None

class StreamEndEvent(BaseModel):
    type: Literal["end"]

StreamResponse = Union[
    StreamSourceEvent,
    StreamAnswerEvent,
    StreamIdEvent,
    StreamErrorEvent,
    StreamEndEvent
]