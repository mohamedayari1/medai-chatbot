from app.core.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls):
        """      
        Implement singleton pattern to ensure only one database connection is created
        This prevents creating multiple unnecessary connections and helps manage resources efficiently
        """
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.MONGO_URI)
        return cls._client
    
    @classmethod
    def close_client(cls):
        """
        Close the MongoDB client connection if it exists
        """
        if cls._client is not None:
            cls._client.close()
            cls._client = None
