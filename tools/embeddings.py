import os
import json
import torch
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(jsonl_file):
    documents = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            doc = json.loads(line)
            documents.append(doc)
    return documents

def chunk_documents(documents, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunked_docs = []
    for doc in documents:
        chunks = text_splitter.split_text(doc['body'])
        for i, chunk_text in enumerate(chunks):
            chunked_docs.append({
                "chunk_id": f"{doc['doc_id']}-{i}",
                "doc_id": doc['doc_id'],
                "text": chunk_text,
                "source_type": doc.get('source_type', 'unknown'),
                "title": doc.get('title', 'Untitled'),
                "created_at": doc.get('created_at'),
                "chunk_index": i
            })
    return chunked_docs

def generate_embeddings(chunked_docs):
    texts = [doc['text'] for doc in chunked_docs]
    embeddings = model.encode(texts)
    
    for i, doc in enumerate(chunked_docs):
        doc['embedding'] = embeddings[i].tolist()
    
    return chunked_docs

def setup_qdrant():
    client = QdrantClient(":memory:") 
    
    client.create_collection(
        collection_name="documents",
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )

    return client

def upload_to_qdrant(client, docs_with_embeddings):
    points = []
    
    for i, doc in enumerate(docs_with_embeddings):
        points.append(
            models.PointStruct(
                id=i,
                vector=doc['embedding'],
                payload={
                    "chunk_id": doc["chunk_id"],
                    "doc_id": doc["doc_id"],
                    "text": doc["text"],
                    "title": doc["title"],
                    "source_type": doc["source_type"],
                    "created_at": doc["created_at"],
                    "chunk_index": doc["chunk_index"]
                }
            )
        )
    
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i+batch_size]
        client.upsert(
            collection_name="documents",
            points=batch
        )
    
    print(f"Uploaded {len(points)} document chunks to Qdrant")

if __name__ == "__main__":
    docs = load_documents('data/parsed_docs.jsonl')
    print(f"Loaded {len(docs)} documents")
    
    chunked_docs = chunk_documents(docs)
    print(f"Created {len(chunked_docs)} chunks")
    
    docs_with_embeddings = generate_embeddings(chunked_docs)
    
    client = setup_qdrant()
    upload_to_qdrant(client, docs_with_embeddings)
    
    print("Embedding and indexing completed")