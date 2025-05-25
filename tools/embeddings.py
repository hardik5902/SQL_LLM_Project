import json
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(jsonl_file: str) -> List[Dict]:
    with open(jsonl_file, 'r') as file:
        return [json.loads(line) for line in file]

def chunk_document(text: str, chunk_size: int = 500) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)

def process_document(client: QdrantClient, text: str, doc_id: int):
    chunks = chunk_document(text)

    embeddings = model.encode(chunks)
    
    # Prepare points with metadata
    points = [
        models.PointStruct(
            id=i,
            vector=embedding.tolist(),
            payload={
                "text": chunk,
                "doc_id": doc_id,
                "chunk_id": i,
                "position": i,
                "total_chunks": len(chunks)
            }
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    client.upsert(
        collection_name="documents",
        points=points
    )

def initialize_qdrant() -> QdrantClient:
    client = QdrantClient(host="localhost", port=6333)

    sample_embedding = model.encode(["sample text"])[0]
    
    client.recreate_collection(
        collection_name="documents",
        vectors_config=models.VectorParams(
            size=len(sample_embedding),
            distance=models.Distance.COSINE
        )
    )
    return client

if __name__ == "__main__":
    client = initialize_qdrant()
    docs = load_documents('data/parsed_docs.jsonl')
    
    for i, doc in enumerate(docs):
        process_document(client, doc['body'], doc_id=i)
        print(f"Processed document {i+1}/{len(docs)}")
    
    print("Indexing completed")


# docker run -p 6333:6333 qdrant/qdrant
# python tools/embeddings.py