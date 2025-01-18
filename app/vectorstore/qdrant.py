from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Batch, Distance, VectorParams

from app.utils.logging import get_logger
from app.core.settings import settings

logger = get_logger(__name__)


class QdrantDatabaseConnector:
    _instance: QdrantClient | None = None

    def __init__(self) -> None:
        if self._instance is None:
            try:
                if settings.USE_QDRANT_CLOUD:
                    self._instance = QdrantClient(
                        url=settings.QDRANT_CLOUD_URL,
                        api_key=settings.QDRANT_APIKEY,
                    )
                else:
                    self._instance = QdrantClient(
                        host=settings.QDRANT_DATABASE_HOST,
                        port=settings.QDRANT_DATABASE_PORT,
                    )
            except UnexpectedResponse:
                logger.exception(
                    "Couldn't connect to Qdrant.",
                    host=settings.QDRANT_DATABASE_HOST,
                    port=settings.QDRANT_DATABASE_PORT,
                    url=settings.QDRANT_CLOUD_URL,
                )

                raise

    def get_collection(self, collection_name: str):
        return self._instance.get_collection(collection_name=collection_name)

    def create_non_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name, vectors_config={}
        )

    def create_vector_collection(self, collection_name: str):
        self._instance.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_SIZE, distance=Distance.COSINE
            ),
        )

    def write_data(self, collection_name: str, points: Batch):
        try:
            self._instance.upsert(collection_name=collection_name, points=points)
        except Exception:
            logger.exception("An error occurred while inserting data.")

            raise

    def search(
        self,
        collection_name: str,
        query_vector: list,
        query_filter: models.Filter | None = None,
        limit: int = 3,
    ) -> list:
        return self._instance.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
        )

    def scroll(self, collection_name: str, limit: int):
        return self._instance.scroll(collection_name=collection_name, limit=limit)

    def close(self):
        if self._instance:
            self._instance.close()

            logger.info("Connected to database has been closed.")


from langchain_community.vectorstores.qdrant import Qdrant
from app.vectorstore.base import BaseVectorStore
from app.core.settings import settings
from qdrant_client import models


class QdrantStore(BaseVectorStore):
    def __init__(self, source_id: str = "", embeddings_key: str = "embeddings"):
        self._filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.source_id",
                    match=models.MatchValue(value=source_id.replace("application/indexes/", "").rstrip("/")),
                )
            ]
        )

        self._docsearch = Qdrant.construct_instance(
            ["TEXT_TO_OBTAIN_EMBEDDINGS_DIMENSION"],
            embedding=self._get_embeddings(settings.EMBEDDINGS_NAME, embeddings_key),
            collection_name=settings.QDRANT_COLLECTION_NAME,
            location=settings.QDRANT_LOCATION,
            url=settings.QDRANT_URL,
            port=settings.QDRANT_PORT,
            grpc_port=settings.QDRANT_GRPC_PORT,
            https=settings.QDRANT_HTTPS,
            prefer_grpc=settings.QDRANT_PREFER_GRPC,
            api_key=settings.QDRANT_API_KEY,
            prefix=settings.QDRANT_PREFIX,
            timeout=settings.QDRANT_TIMEOUT,
            path=settings.QDRANT_PATH,
            distance_func=settings.QDRANT_DISTANCE_FUNC,
        )

    def search(self, *args, **kwargs):
        return self._docsearch.similarity_search(filter=self._filter, *args, **kwargs)

    def add_texts(self, *args, **kwargs):
        return self._docsearch.add_texts(*args, **kwargs)

    def save_local(self, *args, **kwargs):
        pass

    def delete_index(self, *args, **kwargs):
        return self._docsearch.client.delete(
            collection_name=settings.QDRANT_COLLECTION_NAME, points_selector=self._filter
        )
