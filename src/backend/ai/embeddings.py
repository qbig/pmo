"""Semantic embedding for search and similarity."""

import logging
from typing import List, Optional
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available. Install with: pip install sentence-transformers")


class EmbeddingModel:
    """Semantic embedding model for text search."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: Model name (default: all-MiniLM-L6-v2, a small fast model)
        """
        self.model_name = model_name
        self.model: Optional[object] = None
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
                logger.info(f"Loaded embedding model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                self.model = None
        else:
            logger.warning("sentence-transformers not available, embeddings disabled")
    
    def encode(self, texts: List[str]) -> Optional[np.ndarray]:
        """
        Encode texts to embeddings.
        
        Args:
            texts: List of text strings
            
        Returns:
            Numpy array of embeddings (None if model not available)
        """
        if not self.model:
            return None
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            return None
    
    def encode_single(self, text: str) -> Optional[np.ndarray]:
        """Encode a single text."""
        return self.encode([text])
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        # Cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))


class SemanticSearch:
    """Semantic search over indexed files."""
    
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
        self.embeddings_cache: dict = {}  # file_id -> embedding
    
    def index_file(self, file_id: str, content: str):
        """
        Index a file's content for semantic search.
        
        Args:
            file_id: File ID
            content: File content to index
        """
        if not self.embedding_model.model:
            return
        
        # Extract meaningful text (first 500 chars for efficiency)
        text = content[:500] if len(content) > 500 else content
        
        embedding = self.embedding_model.encode_single(text)
        if embedding is not None:
            self.embeddings_cache[file_id] = embedding[0]  # Remove batch dimension
            logger.debug(f"Indexed embedding for {file_id}")
    
    def search(self, query: str, file_embeddings: dict, top_k: int = 5) -> List[tuple]:
        """
        Search for similar files.
        
        Args:
            query: Search query
            file_embeddings: Dict of file_id -> embedding
            top_k: Number of results to return
            
        Returns:
            List of (file_id, similarity_score) tuples, sorted by similarity
        """
        if not self.embedding_model.model:
            return []
        
        query_embedding = self.embedding_model.encode_single(query)
        if query_embedding is None:
            return []
        
        query_embedding = query_embedding[0]  # Remove batch dimension
        
        # Calculate similarities
        results = []
        for file_id, file_embedding in file_embeddings.items():
            similarity = self.embedding_model.similarity(query_embedding, file_embedding)
            results.append((file_id, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def remove_file(self, file_id: str):
        """Remove file from search index."""
        if file_id in self.embeddings_cache:
            del self.embeddings_cache[file_id]
