
from typing import List


class Settings:
    BROKER: str =  "redis://localhost:6379/0"
    BACKEND: int = "redis://localhost:6379/0"
    INCLUDE: List[str] = ["worker.tasks"]


settings = Settings()
