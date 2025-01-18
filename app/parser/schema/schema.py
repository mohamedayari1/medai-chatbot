from typing import Any, Dict, List, Optional
from pydantic import BaseModel, validator

class BaseDocument(BaseModel):
    """Base document.

    Generic abstract interfaces that captures both index structs
    as well as documents.

    """
    text: Optional[str] = None
    doc_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    extra_info: Optional[Dict[str, Any]] = None

    @validator('text')
    def validate_text(cls, v):
        if v is None:
            raise ValueError("text field not set.")
        return v

    @validator('doc_id')
    def validate_doc_id(cls, v):
        if v is None:
            raise ValueError("doc_id not set.")
        return v

    @validator('embedding')
    def validate_embedding(cls, v):
        if v is None:
            raise ValueError("embedding not set.")
        return v

    @property
    def is_doc_id_none(self) -> bool:
        """Check if doc_id is None."""
        return self.doc_id is None

    @property
    def extra_info_str(self) -> Optional[str]:
        """Extra info string."""
        if self.extra_info is None:
            return None
        return "\n".join([f"{k}: {str(v)}" for k, v in self.extra_info.items()])

    class Config:
        arbitrary_types_allowed = True