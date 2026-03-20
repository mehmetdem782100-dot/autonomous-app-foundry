import asyncio
import chromadb
from core.logger import get_logger

logger = get_logger("VECTOR_DB")

class VectorDBClient:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_data")
        logger.info("ChromaDB kalıcı istemcisi başlatıldı.")

    def _get_collection_sync(self, collection_name: str):
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    async def get_or_create_collection_async(self, collection_name: str):
        try:
            collection = await asyncio.to_thread(self._get_collection_sync, collection_name)
            return collection
        except Exception as e:
            logger.error(f"Koleksiyon oluşturulurken asenkron hata: {str(e)}")
            raise

vector_db = VectorDBClient()
