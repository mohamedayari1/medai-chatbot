from pydantic import BaseModel

class UploadModel(BaseModel):
    user: str
    name: str
