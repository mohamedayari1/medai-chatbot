# schemas/search.py
from app.schemas.base import Source
from typing import List, Optional
from pydantic import BaseModel, Field

class SearchRequest(BaseModel):
    question: str = Field(..., description="The question to search")
    chunks: int = Field(default=2, ge=0, description="Number of chunks to retrieve")
    api_key: Optional[str] = None
    active_docs: Optional[str] = None
    retriever: str = Field(default="classic", description="Type of retriever to use")
    token_limit: Optional[int] = Field(None, gt=0)
    isNoneDoc: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "question": "How to implement authentication?",
                "chunks": 2,
                "retriever": "classic"
            }
        }


class SearchResponse(BaseModel):
    results: List[Source]

    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "source": "auth_docs.md",
                        "text": "Authentication can be implemented...",
                        "metadata": {"section": "Authentication"}
                    }
                ]
            }
        }