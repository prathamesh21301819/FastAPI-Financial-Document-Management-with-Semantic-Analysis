from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = QdrantClient(":memory:")

client.create_collection(
    collection_name="Financial_Documents",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

def store_vectors(chunks, embeddings):

    points = []

    for i, (chunk, vector) in enumerate(
        zip(chunks, embeddings)
    ):
        points.append(
            PointStruct(
                id=i,
                vector=vector.tolist(),
                payload={
                    "text": chunk
                }
            )
        )

    client.upsert(
        collection_name="Financial_Documents",
        points=points
    )

    print("✅ Vectors Stored Successfully")
def search_vectors(query):

    query_vector = model.encode(query)

    results = client.search(
        collection_name="Financial_Documents",
        query_vector=query_vector.tolist(),
        limit=5
    )

    return results