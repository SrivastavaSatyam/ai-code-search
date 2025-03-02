import numpy as np
import os
from typing import List, Tuple
from models.code_embedder import CodeEmbedder
from config import settings

class SearchEngine:
    def __init__(self):
        self.embedder = CodeEmbedder()
        self.embeddings = None
        self.code_snippets = []
        
        # Try to load existing index if it exists
        try:
            if os.path.exists(settings.FAISS_INDEX_PATH):
                self.load_index()
                print(f"Loaded existing index with {len(self.code_snippets)} code snippets")
        except Exception as e:
            print(f"Could not load existing index: {str(e)}")
    
    def cosine_similarity(self, query_embedding: np.ndarray) -> np.ndarray:
        # Compute cosine similarity between query and all stored embeddings
        norm_query = np.linalg.norm(query_embedding, axis=1, keepdims=True)
        norm_embeddings = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        dot_product = np.dot(query_embedding, self.embeddings.T)
        similarities = dot_product / (norm_query * norm_embeddings.T + 1e-8)
        return similarities[0]  # Return 1D array of similarities
    
    def add_code(self, code_snippets: List[str]):
        if not code_snippets:
            return
            
        try:
            new_embeddings = self.embedder.get_embeddings(code_snippets)
            
            if self.embeddings is None:
                self.embeddings = new_embeddings
            else:
                self.embeddings = np.vstack([self.embeddings, new_embeddings])
                
            self.code_snippets.extend(code_snippets)
            print(f"Added {len(code_snippets)} code snippets. Total: {len(self.code_snippets)}")
        except Exception as e:
            print(f"Error adding code: {str(e)}")
            raise
    
    def search(self, query: str, k: int = None) -> List[Tuple[str, float]]:
        if k is None:
            k = settings.TOP_K_RESULTS
            
        if not self.code_snippets or self.embeddings is None:
            return []
            
        query_embedding = self.embedder.get_embeddings(query)
        similarities = self.cosine_similarity(query_embedding)
        
        # Get top k indices and scores
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            if idx < len(self.code_snippets):
                results.append((self.code_snippets[idx], float(similarities[idx])))
        
        return results
    
    def save_index(self, path: str = None):
        if path is None:
            path = str(settings.FAISS_INDEX_PATH)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save embeddings and code snippets using numpy
        save_data = {
            'embeddings': self.embeddings,
            'code_snippets': np.array(self.code_snippets, dtype=object)
        }
        np.save(path, save_data, allow_pickle=True)
        print(f"Index saved to {path}")
    
    def load_index(self, path: str = None):
        if path is None:
            path = str(settings.FAISS_INDEX_PATH)
        
        # Load embeddings and code snippets
        loaded_data = np.load(path, allow_pickle=True).item()
        self.embeddings = loaded_data['embeddings']
        self.code_snippets = loaded_data['code_snippets'].tolist() 