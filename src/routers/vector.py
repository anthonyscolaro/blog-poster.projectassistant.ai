"""
Vector search endpoints
"""
import logging
from fastapi import APIRouter, HTTPException

from ..models import IndexDocumentRequest, SearchDocumentsRequest
from src.services.vector_search import VectorSearchManager, SearchResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vector", tags=["vector"])

# Global vector search manager
vector_manager = None

def get_vector_manager():
    """Get or create vector search manager"""
    global vector_manager
    if vector_manager is None:
        vector_manager = VectorSearchManager()
    return vector_manager


@router.post("/index")
async def index_document(request: IndexDocumentRequest):
    """
    Index a document in vector search
    
    Args:
        content: Document content
        document_id: Unique document ID
        title: Document title
        url: Document URL
        collection: Collection to index in
    """
    manager = get_vector_manager()
    
    success = await manager.index_document(
        content=request.content,
        document_id=request.document_id,
        title=request.title,
        url=request.url,
        collection=request.collection
    )
    
    if success:
        return {
            "success": True,
            "message": f"Document {request.document_id} indexed successfully",
            "collection": request.collection
        }
    else:
        raise HTTPException(500, "Failed to index document")


@router.post("/search")
async def search_documents(request: SearchDocumentsRequest):
    """
    Search for similar documents
    
    Args:
        query: Search query
        limit: Number of results
        collection: Collection to search
    """
    manager = get_vector_manager()
    
    results = await manager.search(
        query=request.query,
        limit=request.limit,
        collection=request.collection
    )
    
    return {
        "query": request.query,
        "results": [
            {
                "title": r.document_title,
                "content": r.content[:200] + "...",
                "url": r.document_url,
                "score": r.similarity_score
            }
            for r in results
        ],
        "count": len(results)
    }


@router.post("/check-duplicate")
async def check_duplicate(
    content: str,
    threshold: float = 0.9,
    collection: str = "blog_articles"
):
    """
    Check if content is duplicate
    
    Args:
        content: Content to check
        threshold: Similarity threshold (0.9 = 90% similar)
        collection: Collection to check against
    """
    manager = get_vector_manager()
    
    duplicate = await manager.check_duplicate(
        content=content,
        threshold=threshold,
        collection=collection
    )
    
    if duplicate:
        return {
            "is_duplicate": True,
            "similar_document": {
                "title": duplicate.document_title,
                "url": duplicate.document_url,
                "similarity": duplicate.similarity_score
            }
        }
    else:
        return {
            "is_duplicate": False,
            "message": "No duplicate found"
        }


@router.get("/internal-links")
async def get_internal_links(
    content: str,
    limit: int = 5
):
    """
    Get internal link recommendations based on content
    
    Args:
        content: Content to find links for
        limit: Maximum number of links
    """
    manager = get_vector_manager()
    
    links = await manager.get_internal_links(
        content=content,
        limit=limit
    )
    
    return {
        "links": links,
        "count": len(links)
    }


@router.get("/stats")
async def get_vector_stats(collection: str = "blog_articles"):
    """
    Get collection statistics
    
    Args:
        collection: Collection name
    """
    manager = get_vector_manager()
    stats = manager.get_collection_stats(collection)
    
    return stats


@router.delete("/document/{document_id}")
async def delete_document(
    document_id: str,
    collection: str = "blog_articles"
):
    """
    Delete a document from vector search
    
    Args:
        document_id: Document ID to delete
        collection: Collection to delete from
    """
    manager = get_vector_manager()
    
    success = await manager.delete_document(
        document_id=document_id,
        collection=collection
    )
    
    if success:
        return {
            "success": True,
            "message": f"Document {document_id} deleted"
        }
    else:
        raise HTTPException(500, "Failed to delete document")