from typing import List, Dict
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.client = QdrantClient(
            host="localhost",
            port=6333,
            timeout=10
        )
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name
        )
        
    def create_store(self) -> Qdrant:
        return Qdrant(
            client=self.client,
            collection_name="documents",
            embeddings=self.embeddings
        )
    
    def search(self, query: str, limit: int = 3, threshold: float = 0.7) -> List[Dict]:
        query_embedding = self.model.encode([query])[0]
        
        search_results = self.client.search(
            collection_name="documents",
            query_vector=query_embedding.tolist(),
            limit=limit,
            score_threshold=threshold
        )
        return search_results
    
    def display_results(self, results: List[Dict]) -> None:
        print(f"\nFound {len(results)} relevant results:")
        for result in results:
            print(f"\nRelevance Score: {result.score:.2f}")
            print(f"Document: Chunk {result.payload['chunk_id']+1}/{result.payload['total_chunks']}")
            print(f"Text: {result.payload['text']}\n")
            print("-" * 80)

if __name__ == "__main__":
    retriever = VectorRetriever()
    query = "Who are the authors of the parkinson's paper?"
    results = retriever.search(query)
    retriever.display_results(results)