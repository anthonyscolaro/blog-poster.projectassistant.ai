"""
Repository pattern for database operations
Provides clean interface for data access
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
import logging
import json

from .models import Article, Pipeline, ApiKey, CompetitorArticle

logger = logging.getLogger(__name__)


class ArticleRepository:
    """Repository for Article operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, article_data: Dict[str, Any]) -> Article:
        """Create a new article"""
        try:
            article = Article(**article_data)
            self.db.add(article)
            self.db.commit()
            self.db.refresh(article)
            logger.info(f"Created article: {article.slug}")
            return article
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create article: {e}")
            raise
    
    def get_by_id(self, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        return self.db.query(Article).filter(Article.id == article_id).first()
    
    def get_by_slug(self, slug: str) -> Optional[Article]:
        """Get article by slug"""
        return self.db.query(Article).filter(Article.slug == slug).first()
    
    def get_recent(self, limit: int = 50, offset: int = 0) -> List[Article]:
        """Get recent articles"""
        return self.db.query(Article)\
            .order_by(desc(Article.created_at))\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    def get_by_status(self, status: str, limit: int = 50) -> List[Article]:
        """Get articles by status"""
        return self.db.query(Article)\
            .filter(Article.status == status)\
            .order_by(desc(Article.created_at))\
            .limit(limit)\
            .all()
    
    def update(self, article_id: int, updates: Dict[str, Any]) -> Optional[Article]:
        """Update an article"""
        try:
            article = self.get_by_id(article_id)
            if not article:
                return None
            
            for key, value in updates.items():
                if hasattr(article, key):
                    setattr(article, key, value)
            
            article.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(article)
            logger.info(f"Updated article: {article.slug}")
            return article
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update article {article_id}: {e}")
            raise
    
    def delete(self, article_id: int) -> bool:
        """Delete an article"""
        try:
            article = self.get_by_id(article_id)
            if not article:
                return False
            
            self.db.delete(article)
            self.db.commit()
            logger.info(f"Deleted article: {article.slug}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to delete article {article_id}: {e}")
            raise
    
    def search(self, query: str, limit: int = 10) -> List[Article]:
        """Search articles by title or content"""
        search_pattern = f"%{query}%"
        return self.db.query(Article)\
            .filter(or_(
                Article.title.ilike(search_pattern),
                Article.content_markdown.ilike(search_pattern),
                Article.primary_keyword.ilike(search_pattern)
            ))\
            .limit(limit)\
            .all()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get article statistics"""
        total = self.db.query(Article).count()
        published = self.db.query(Article).filter(Article.status == 'published').count()
        draft = self.db.query(Article).filter(Article.status == 'draft').count()
        
        # Articles in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent = self.db.query(Article)\
            .filter(Article.created_at >= thirty_days_ago)\
            .count()
        
        return {
            'total': total,
            'published': published,
            'draft': draft,
            'recent_30_days': recent
        }


class PipelineRepository:
    """Repository for Pipeline operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, pipeline_data: Dict[str, Any]) -> Pipeline:
        """Create a new pipeline record"""
        try:
            # Generate pipeline_id if not provided
            if 'pipeline_id' not in pipeline_data:
                pipeline_data['pipeline_id'] = f"pipeline_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            pipeline = Pipeline(**pipeline_data)
            self.db.add(pipeline)
            self.db.commit()
            self.db.refresh(pipeline)
            logger.info(f"Created pipeline: {pipeline.pipeline_id}")
            return pipeline
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create pipeline: {e}")
            raise
    
    def get_by_id(self, pipeline_id: int) -> Optional[Pipeline]:
        """Get pipeline by database ID"""
        return self.db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    
    def get_by_pipeline_id(self, pipeline_id: str) -> Optional[Pipeline]:
        """Get pipeline by pipeline_id string"""
        return self.db.query(Pipeline).filter(Pipeline.pipeline_id == pipeline_id).first()
    
    def get_recent(self, limit: int = 20) -> List[Pipeline]:
        """Get recent pipeline executions"""
        return self.db.query(Pipeline)\
            .order_by(desc(Pipeline.created_at))\
            .limit(limit)\
            .all()
    
    def get_active(self) -> List[Pipeline]:
        """Get currently running pipelines"""
        return self.db.query(Pipeline)\
            .filter(Pipeline.status.in_(['running', 'pending']))\
            .order_by(desc(Pipeline.started_at))\
            .all()
    
    def update_status(self, pipeline_id: str, status: str, **kwargs) -> Optional[Pipeline]:
        """Update pipeline status and optional fields"""
        try:
            pipeline = self.get_by_pipeline_id(pipeline_id)
            if not pipeline:
                return None
            
            pipeline.status = status
            
            # Update optional fields
            for key, value in kwargs.items():
                if hasattr(pipeline, key):
                    setattr(pipeline, key, value)
            
            # Set completed_at if status is terminal
            if status in ['completed', 'failed', 'cancelled']:
                pipeline.completed_at = datetime.utcnow()
                if pipeline.started_at:
                    pipeline.execution_time_seconds = (
                        pipeline.completed_at - pipeline.started_at
                    ).total_seconds()
            
            self.db.commit()
            self.db.refresh(pipeline)
            return pipeline
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update pipeline {pipeline_id}: {e}")
            raise
    
    def get_cost_stats(self, days: int = 30) -> Dict[str, float]:
        """Get cost statistics for the last N days"""
        since = datetime.utcnow() - timedelta(days=days)
        
        pipelines = self.db.query(Pipeline)\
            .filter(Pipeline.created_at >= since)\
            .all()
        
        total_cost = sum(p.total_cost or 0 for p in pipelines)
        total_tokens = sum(p.llm_tokens_used or 0 for p in pipelines)
        
        return {
            'total_cost': total_cost,
            'total_tokens': total_tokens,
            'pipeline_count': len(pipelines),
            'avg_cost_per_pipeline': total_cost / len(pipelines) if pipelines else 0
        }


class ApiKeyRepository:
    """Repository for API Key operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def upsert(self, service: str, encrypted_key: str, key_preview: str = None) -> ApiKey:
        """Create or update an API key"""
        try:
            api_key = self.db.query(ApiKey).filter(ApiKey.service == service).first()
            
            if api_key:
                # Update existing
                api_key.encrypted_key = encrypted_key
                api_key.key_preview = key_preview
                api_key.updated_at = datetime.utcnow()
            else:
                # Create new
                api_key = ApiKey(
                    service=service,
                    encrypted_key=encrypted_key,
                    key_preview=key_preview
                )
                self.db.add(api_key)
            
            self.db.commit()
            self.db.refresh(api_key)
            logger.info(f"Saved API key for service: {service}")
            return api_key
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to save API key for {service}: {e}")
            raise
    
    def get_by_service(self, service: str) -> Optional[ApiKey]:
        """Get API key by service name"""
        return self.db.query(ApiKey)\
            .filter(and_(ApiKey.service == service, ApiKey.is_active == True))\
            .first()
    
    def get_all_active(self) -> List[ApiKey]:
        """Get all active API keys"""
        return self.db.query(ApiKey)\
            .filter(ApiKey.is_active == True)\
            .all()
    
    def deactivate(self, service: str) -> bool:
        """Deactivate an API key"""
        try:
            api_key = self.get_by_service(service)
            if not api_key:
                return False
            
            api_key.is_active = False
            api_key.updated_at = datetime.utcnow()
            self.db.commit()
            logger.info(f"Deactivated API key for service: {service}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to deactivate API key for {service}: {e}")
            raise
    
    def update_usage(self, service: str) -> None:
        """Update usage statistics for an API key"""
        try:
            api_key = self.get_by_service(service)
            if api_key:
                api_key.last_used_at = datetime.utcnow()
                api_key.usage_count = (api_key.usage_count or 0) + 1
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to update usage for {service}: {e}")


class CompetitorRepository:
    """Repository for Competitor Article operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, article_data: Dict[str, Any]) -> CompetitorArticle:
        """Create a new competitor article record"""
        try:
            article = CompetitorArticle(**article_data)
            self.db.add(article)
            self.db.commit()
            self.db.refresh(article)
            logger.info(f"Tracked competitor article: {article.url}")
            return article
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create competitor article: {e}")
            raise
    
    def get_by_url(self, url: str) -> Optional[CompetitorArticle]:
        """Get competitor article by URL"""
        return self.db.query(CompetitorArticle).filter(CompetitorArticle.url == url).first()
    
    def get_by_domain(self, domain: str, limit: int = 50) -> List[CompetitorArticle]:
        """Get articles from a specific competitor"""
        return self.db.query(CompetitorArticle)\
            .filter(CompetitorArticle.competitor_domain == domain)\
            .order_by(desc(CompetitorArticle.discovered_at))\
            .limit(limit)\
            .all()
    
    def get_recent(self, days: int = 30, limit: int = 100) -> List[CompetitorArticle]:
        """Get recently discovered competitor articles"""
        since = datetime.utcnow() - timedelta(days=days)
        return self.db.query(CompetitorArticle)\
            .filter(CompetitorArticle.discovered_at >= since)\
            .order_by(desc(CompetitorArticle.discovered_at))\
            .limit(limit)\
            .all()
    
    def get_trending_topics(self, days: int = 7) -> List[Dict[str, Any]]:
        """Analyze trending topics from competitor articles"""
        since = datetime.utcnow() - timedelta(days=days)
        articles = self.db.query(CompetitorArticle)\
            .filter(CompetitorArticle.discovered_at >= since)\
            .all()
        
        # Aggregate topics
        topic_counts = {}
        for article in articles:
            if article.main_topics:
                for topic in article.main_topics:
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Sort by frequency
        trending = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'topic': topic, 'count': count, 'trend': 'rising'}
            for topic, count in trending[:10]
        ]