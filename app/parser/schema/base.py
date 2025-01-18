from pydantic import BaseModel, validator
from langchain.docstore.document import Document as LCDocument

from app.parser.schema.schema import BaseDocument

class Document(BaseDocument):
    """Generic interface for a data document.

    This document connects to data sources.

    """

    @validator('text', pre=True, always=True)
    def validate_text(cls, v):
        if v is None:
            raise ValueError("text field not set.")
        return v

    @classmethod
    def get_type(cls) -> str:
        """Get Document type."""
        return "Document"

    def to_langchain_format(self) -> LCDocument:
        """Convert struct to LangChain document format."""
        metadata = self.extra_info or {}
        return LCDocument(page_content=self.text, metadata=metadata)

    @classmethod
    def from_langchain_format(cls, doc: LCDocument) -> "Document":
        """Convert struct from LangChain document format."""
        return cls(text=doc.page_content, extra_info=doc.metadata)

    class Config:
        arbitrary_types_allowed = True