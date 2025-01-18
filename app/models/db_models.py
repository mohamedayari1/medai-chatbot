from pydantic import BaseModel, Field
from typing import List

class QnA(BaseModel):
    prompt: str
    response: str

class Conversation(BaseModel):
    userId: str
    qna_list: List[QnA] = Field(default_factory=list)