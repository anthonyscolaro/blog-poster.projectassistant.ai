"""
Vector Search Integration with Qdrant

Provides semantic search capabilities for content similarity,
duplicate detection, and internal linking recommendations.
"""
import os
import logging
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json

import httpx
from pydantic import BaseModel, Field
import numpy as np
import asyncpg
from typing import Tuple
import psycopg2
from psycopg2.extras import RealDictCursor

# For embeddings, we'll use OpenAI or a local model
try:
    import openai
    from openai import OpenAI
except ImportError:
    openai = None

logger = logging.getLogger(__name__)


class DocumentChunk(BaseModel):
    """A chunk of document content with metadata"""
    content: str
    chunk_id: str
    document_id: str
    document_title: str
    document_url: Optional[str] = None
    chunk_index: int
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)


class SearchResult(BaseModel):
    """A search result from vector similarity"""
    content: str
    document_id: str
    document_title: str
    document_url: Optional[str] = None
    similarity_score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VectorSearchManager:
    """
    Manages vector search operations with pgvector in PostgreSQL
    """
    
    # Table names (replacing Qdrant collections)
    ARTICLES_TABLE = "articles"
    COMPETITORS_TABLE = "competitor_content"
    RESEARCH_TABLE = "research_docs"
    
    # Embedding configuration
    EMBEDDING_DIMENSION = 1536  # OpenAI ada-002 dimension
    CHUNK_SIZE = 500  # Characters per chunk
    CHUNK_OVERLAP = 100  # Overlap between chunks
    
    def __init__(
        self,
        database_url: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        table_name: Optional[str] = None
    ):
        """
        Initialize the vector search manager
        
        Args:
            database_url: PostgreSQL connection URL
            openai_api_key: OpenAI API key for embeddings
            table_name: Default table to use
        """
        # Database connection
        self.database_url = database_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5434/postgres")
        self.conn = None
        self._connect()
        logger.info(f"Connected to PostgreSQL with pgvector")
        
        # OpenAI client for embeddings
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.openai_client = None
        if self.openai_api_key and openai:
            try:
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                logger.info("OpenAI client initialized for embeddings")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI client: {e}")
        
        # Default table
        self.table_name = table_name or self.ARTICLES_TABLE
        
        # Ensure pgvector extension is enabled
        self._initialize_pgvector()
    
    def _initialize_collections(self):
        """Initialize Qdrant collections if they don't exist"""
        collections = [
            self.ARTICLES_COLLECTION,
            self.COMPETITORS_COLLECTION,
            self.RESEARCH_COLLECTION
        ]
        
        for collection in collections:
            try:
                # Check if collection exists
                collection_info = self.client.get_collection(collection)
                logger.info(f"Collection '{collection}' exists with {collection_info.points_count} points")
            except Exception:
                # Create collection
                try:
                    self.client.create_collection(
                        collection_name=collection,
                        vectors_config=VectorParams(
                            size=self.EMBEDDING_DIMENSION,
                            distance=Distance.COSINE
                        )
                    )
                    logger.info(f"Created collection '{collection}'")
                except Exception as e:
                    logger.error(f"Failed to create collection '{collection}': {e}")
    
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector or None if failed
        """
        if not self.openai_client:
            # Fallback to random embedding for testing
            logger.warning("No OpenAI client, using random embedding")
            return np.random.randn(self.EMBEDDING_DIMENSION).tolist()
        
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            # Fallback to random
            return np.random.randn(self.EMBEDDING_DIMENSION).tolist()
    
    def chunk_text(self, text: str, chunk_size: Optional[int] = None) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or self.CHUNK_SIZE
        chunks = []
        
        # Clean text
        text = text.strip()
        if not text:
            return []
        
        # Split into chunks with overlap
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end
                for punct in ['. ', '! ', '? ', '\n\n']:
                    last_punct = text[start:end].rfind(punct)
                    if last_punct > chunk_size // 2:
                        end = start + last_punct + len(punct) - 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start with overlap
            start = end - self.CHUNK_OVERLAP if end < len(text) else end
        
        return chunks
    
    async def index_document(
        self,
        content: str,
        document_id: str,
        title: str,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        collection: Optional[str] = None
    ) -> bool:
        """
        Index a document in Qdrant
        
        Args:
            content: Document content
            document_id: Unique document ID
            title: Document title
            url: Document URL
            metadata: Additional metadata
            collection: Collection to use
            
        Returns:
            Success status
        """
        collection = collection or self.collection_name
        metadata = metadata or {}
        
        try:
            # Chunk the content
            chunks = self.chunk_text(content)
            if not chunks:
                logger.warning(f"No chunks generated for document {document_id}")
                return False
            
            logger.info(f"Indexing {len(chunks)} chunks for document: {title}")
            
            # Create points for each chunk
            points = []
            for i, chunk_text in enumerate(chunks):
                # Generate embedding
                embedding = await self.generate_embedding(chunk_text)
                if not embedding:
                    continue
                
                # Create unique chunk ID
                chunk_id = hashlib.md5(f"{document_id}_{i}".encode()).hexdigest()
                
                # Create point
                point = PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "content": chunk_text,
                        "document_id": document_id,
                        "document_title": title,
                        "document_url": url,
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "indexed_at": datetime.now().isoformat(),
                        **metadata
                    }
                )
                points.append(point)
            
            # Batch upsert points
            if points:
                self.client.upsert(
                    collection_name=collection,
                    points=points
                )
                logger.info(f"Successfully indexed {len(points)} chunks for {title}")
                return True
            else:
                logger.warning(f"No points created for document {document_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to index document {document_id}: {e}")
            return False
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        collection: Optional[str] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """
        Search for similar content
        
        Args:
            query: Search query
            limit: Number of results
            collection: Collection to search
            filter_metadata: Metadata filters
            
        Returns:
            List of search results
        """
        collection = collection or self.collection_name
        
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Build filter if provided
            filter_conditions = None
            if filter_metadata:
                conditions = []
                for key, value in filter_metadata.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    filter_conditions = Filter(must=conditions)
            
            # Search
            results = self.client.search(
                collection_name=collection,
                query_vector=query_embedding,
                limit=limit,
                query_filter=filter_conditions
            )
            
            # Convert to SearchResult objects
            search_results = []
            for result in results:
                search_results.append(SearchResult(
                    content=result.payload.get("content", ""),
                    document_id=result.payload.get("document_id", ""),
                    document_title=result.payload.get("document_title", ""),
                    document_url=result.payload.get("document_url"),
                    similarity_score=result.score,
                    metadata={
                        k: v for k, v in result.payload.items()
                        if k not in ["content", "document_id", "document_title", "document_url"]
                    }
                ))
            
            return search_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def find_similar_documents(
        self,
        document_id: str,
        limit: int = 5,
        collection: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Find documents similar to a given document
        
        Args:
            document_id: Document ID to find similar to
            limit: Number of results
            collection: Collection to search
            
        Returns:
            List of similar documents
        """
        collection = collection or self.collection_name
        
        try:
            # Get the document's chunks
            document_points = self.client.scroll(
                collection_name=collection,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id)
                        )
                    ]
                ),
                limit=1
            )
            
            if not document_points[0]:
                logger.warning(f"Document {document_id} not found")
                return []
            
            # Use first chunk's embedding for similarity
            point = document_points[0][0]
            
            # Search for similar documents (excluding self)
            results = self.client.search(
                collection_name=collection,
                query_vector=point.vector,
                limit=limit + 10,  # Get extra to filter out self
                query_filter=Filter(
                    must_not=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id)
                        )
                    ]
                )
            )
            
            # Deduplicate by document_id
            seen_docs = set()
            unique_results = []
            for result in results:
                doc_id = result.payload.get("document_id")
                if doc_id not in seen_docs:
                    seen_docs.add(doc_id)
                    unique_results.append(SearchResult(
                        content=result.payload.get("content", ""),
                        document_id=doc_id,
                        document_title=result.payload.get("document_title", ""),
                        document_url=result.payload.get("document_url"),
                        similarity_score=result.score,
                        metadata={
                            k: v for k, v in result.payload.items()
                            if k not in ["content", "document_id", "document_title", "document_url"]
                        }
                    ))
                    
                    if len(unique_results) >= limit:
                        break
            
            return unique_results
            
        except Exception as e:
            logger.error(f"Failed to find similar documents: {e}")
            return []
    
    async def check_duplicate(
        self,
        content: str,
        threshold: float = 0.9,
        collection: Optional[str] = None
    ) -> Optional[SearchResult]:
        """
        Check if content is duplicate or very similar to existing
        
        Args:
            content: Content to check
            threshold: Similarity threshold (0.9 = 90% similar)
            collection: Collection to check
            
        Returns:
            Most similar result if above threshold, None otherwise
        """
        collection = collection or self.collection_name
        
        # Search for similar content
        results = await self.search(
            query=content[:1000],  # Use first 1000 chars
            limit=1,
            collection=collection
        )
        
        if results and results[0].similarity_score >= threshold:
            logger.warning(
                f"Potential duplicate found: {results[0].document_title} "
                f"(similarity: {results[0].similarity_score:.2%})"
            )
            return results[0]
        
        return None
    
    async def get_internal_links(
        self,
        content: str,
        limit: int = 5,
        min_similarity: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Get internal linking recommendations based on content similarity
        
        Args:
            content: Content to find links for
            limit: Maximum number of links
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of link recommendations with title and URL
        """
        # Search in articles collection
        results = await self.search(
            query=content[:1000],
            limit=limit * 2,  # Get extra to filter
            collection=self.ARTICLES_COLLECTION
        )
        
        # Filter and format results
        links = []
        seen_docs = set()
        
        for result in results:
            if result.similarity_score < min_similarity:
                continue
            
            if result.document_id in seen_docs:
                continue
            
            seen_docs.add(result.document_id)
            
            links.append({
                "title": result.document_title,
                "url": result.document_url or f"/article/{result.document_id}",
                "relevance_score": result.similarity_score,
                "excerpt": result.content[:200] + "..."
            })
            
            if len(links) >= limit:
                break
        
        return links
    
    def get_collection_stats(self, collection: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for a collection or all collections
        
        Args:
            collection: Collection name (if None, returns stats for all collections)
            
        Returns:
            Collection statistics
        """
        if collection:
            # Get stats for specific collection
            try:
                info = self.client.get_collection(collection)
                return {
                    "collection": collection,
                    "points_count": info.points_count,
                    "vectors_count": info.vectors_count,
                    "indexed_vectors_count": info.indexed_vectors_count,
                    "status": info.status,
                    "config": {
                        "vector_size": info.config.params.vectors.size,
                        "distance": info.config.params.vectors.distance
                    }
                }
            except Exception as e:
                logger.error(f"Failed to get collection stats: {e}")
                return {"error": str(e)}
        else:
            # Get stats for all collections
            all_stats = {}
            for coll_name in [self.ARTICLES_COLLECTION, self.COMPETITORS_COLLECTION, self.RESEARCH_COLLECTION]:
                try:
                    info = self.client.get_collection(coll_name)
                    all_stats[coll_name] = {
                        "points_count": info.points_count,
                        "vectors_count": info.vectors_count,
                        "status": info.status
                    }
                except Exception as e:
                    logger.warning(f"Collection {coll_name} not found or error: {e}")
                    all_stats[coll_name] = {"points_count": 0, "status": "not_found"}
            return all_stats
    
    async def delete_document(
        self,
        document_id: str,
        collection: Optional[str] = None
    ) -> bool:
        """
        Delete a document from the index
        
        Args:
            document_id: Document ID to delete
            collection: Collection to delete from
            
        Returns:
            Success status
        """
        collection = collection or self.collection_name
        
        try:
            # Delete all points with this document_id
            self.client.delete(
                collection_name=collection,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id)
                        )
                    ]
                )
            )
            logger.info(f"Deleted document {document_id} from {collection}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    def clear_collection(self, collection: Optional[str] = None) -> bool:
        """
        Clear all documents from a collection
        
        Args:
            collection: Collection to clear
            
        Returns:
            Success status
        """
        collection = collection or self.collection_name
        
        try:
            self.client.delete_collection(collection)
            self._initialize_collections()  # Recreate
            logger.info(f"Cleared collection {collection}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection {collection}: {e}")
            return False


# Example usage
async def main():
    """Example of using the vector search manager"""
    
    # Initialize manager
    manager = VectorSearchManager()
    
    # Index a sample article
    article_content = """
    Service dogs are specially trained animals that provide assistance to people with disabilities.
    Under the ADA, service dogs are allowed in all public accommodations. They perform specific
    tasks related to their handler's disability, such as guiding people who are blind, alerting
    people who are deaf, or providing stability for people with mobility issues.
    """
    
    success = await manager.index_document(
        content=article_content,
        document_id="article-001",
        title="Understanding Service Dogs and the ADA",
        url="/articles/understanding-service-dogs",
        metadata={"category": "ADA", "author": "AI"}
    )
    
    print(f"Indexing successful: {success}")
    
    # Search for similar content
    query = "What are the ADA requirements for service animals in restaurants?"
    results = await manager.search(query, limit=3)
    
    print(f"\nSearch results for: '{query}'")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.document_title} (Score: {result.similarity_score:.2%})")
        print(f"   {result.content[:100]}...")
    
    # Check for duplicates
    duplicate_check = "Service dogs help people with disabilities by performing specific tasks."
    duplicate = await manager.check_duplicate(duplicate_check, threshold=0.8)
    
    if duplicate:
        print(f"\nDuplicate found: {duplicate.document_title}")
    else:
        print("\nNo duplicate found")
    
    # Get internal link recommendations
    new_content = "Training a service dog requires patience and consistency. The ADA has specific requirements."
    links = await manager.get_internal_links(new_content, limit=3)
    
    print(f"\nRecommended internal links:")
    for link in links:
        print(f"- {link['title']} ({link['relevance_score']:.2%})")
    
    # Get collection stats
    stats = manager.get_collection_stats()
    print(f"\nCollection stats: {stats}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())