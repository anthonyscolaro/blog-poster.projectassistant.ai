"""
Orchestration Manager with PostgreSQL Integration
Manages the complete article generation pipeline with database persistence
"""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import asyncio
import json

from src.database import get_db_session
from src.database.repositories import ArticleRepository, PipelineRepository
from src.models.pipeline import PipelineResult, PipelineStatus
from src.models.article_models import (
    ArticleRequest,
    Article as ArticleModel,
    TopicRecommendation,
    CompetitorInsights,
    FactCheckReport,
    WordPressResult
)
from src.services.wordpress_publisher import WordPressPublisher
from src.services.pipeline_logger import pipeline_logger

logger = logging.getLogger(__name__)


class OrchestrationManager:
    """
    Manages article generation pipeline with PostgreSQL persistence
    """
    
    def __init__(self):
        self.current_pipeline = None
        self.wp_publisher = WordPressPublisher()
        
    async def run_pipeline(self, request: ArticleRequest) -> PipelineResult:
        """
        Execute the complete pipeline and persist to database
        """
        pipeline_id = f"pipeline_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        
        # Create pipeline record in database
        with get_db_session() as db:
            pipeline_repo = PipelineRepository(db)
            pipeline = pipeline_repo.create({
                'pipeline_id': pipeline_id,
                'status': 'running',
                'started_at': datetime.utcnow(),
                'input_config': request.dict()
            })
            db_pipeline_id = pipeline.id
        
        # Initialize result
        result = PipelineResult(
            pipeline_id=pipeline_id,
            status=PipelineStatus.RUNNING,
            started_at=datetime.utcnow()
        )
        
        try:
            # Log pipeline start
            pipeline_logger.log(
                pipeline_id, 
                'info', 
                f"Starting pipeline for topic: {request.topic or 'auto-generated'}"
            )
            
            # Execute pipeline stages
            result.competitor_insights = await self._run_competitor_monitoring(pipeline_id, request)
            result.topic_recommendation = await self._run_topic_analysis(pipeline_id, request, result.competitor_insights)
            result.article = await self._run_article_generation(pipeline_id, result.topic_recommendation)
            result.fact_check_report = await self._run_fact_checking(pipeline_id, result.article)
            
            # Publish if requested
            if request.auto_publish and result.fact_check_report.is_approved:
                result.wordpress_result = await self._run_wordpress_publishing(pipeline_id, result.article)
            
            # Mark as completed
            result.status = PipelineStatus.COMPLETED
            result.completed_at = datetime.utcnow()
            result.execution_time = (result.completed_at - result.started_at).total_seconds()
            
            # Save article to database
            await self._save_article_to_db(result.article, db_pipeline_id, result.wordpress_result)
            
            # Update pipeline status
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                pipeline_repo.update_status(
                    pipeline_id,
                    'completed',
                    completed_at=result.completed_at,
                    execution_time_seconds=result.execution_time,
                    total_cost=result.total_cost,
                    topic_recommendation=result.topic_recommendation.dict() if result.topic_recommendation else None,
                    fact_check_report=result.fact_check_report.dict() if result.fact_check_report else None,
                    wordpress_result=result.wordpress_result.dict() if result.wordpress_result else None
                )
            
            pipeline_logger.log(pipeline_id, 'success', "Pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline {pipeline_id} failed: {e}")
            result.status = PipelineStatus.FAILED
            result.errors.append(str(e))
            result.completed_at = datetime.utcnow()
            
            # Update pipeline status as failed
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                pipeline_repo.update_status(
                    pipeline_id,
                    'failed',
                    completed_at=result.completed_at,
                    errors=[str(e)]
                )
            
            pipeline_logger.log(pipeline_id, 'error', f"Pipeline failed: {e}")
            
        finally:
            self.current_pipeline = None
            
        return result
    
    async def _save_article_to_db(
        self, 
        article: ArticleModel, 
        pipeline_id: int,
        wp_result: Optional[WordPressResult] = None
    ):
        """Save article to PostgreSQL database"""
        try:
            with get_db_session() as db:
                article_repo = ArticleRepository(db)
                
                article_data = {
                    'title': article.title,
                    'slug': article.slug,
                    'content_markdown': article.content_markdown,
                    'content_html': article.content_html,
                    'excerpt': article.excerpt,
                    'meta_title': article.meta_title,
                    'meta_description': article.meta_description,
                    'primary_keyword': article.primary_keyword,
                    'secondary_keywords': article.secondary_keywords,
                    'seo_score': article.seo_score,
                    'word_count': article.word_count,
                    'reading_time': article.reading_time,
                    'internal_links': article.internal_links_count,
                    'external_links': article.external_links_count,
                    'pipeline_id': pipeline_id,
                    'status': 'published' if wp_result and wp_result.success else 'draft'
                }
                
                # Add WordPress data if published
                if wp_result and wp_result.success:
                    article_data.update({
                        'wp_post_id': wp_result.post_id,
                        'wp_url': wp_result.post_url,
                        'wp_status': 'published',
                        'published_at': datetime.utcnow()
                    })
                
                saved_article = article_repo.create(article_data)
                logger.info(f"Article saved to database: {saved_article.id}")
                
        except Exception as e:
            logger.error(f"Failed to save article to database: {e}")
            # Don't fail the pipeline if database save fails
    
    async def _run_competitor_monitoring(self, pipeline_id: str, request: ArticleRequest) -> Optional[CompetitorInsights]:
        """Run competitor monitoring agent"""
        pipeline_logger.log(pipeline_id, 'info', "Starting competitor monitoring...")
        
        # For now, return mock data - implement real agent later
        return CompetitorInsights(
            competitors_analyzed=3,
            trending_topics=["service dog laws 2024", "ADA compliance updates", "emotional support animals"],
            content_gaps=["service dog training costs", "airline policies 2024"],
            recommended_keywords=["service dog certification", "ADA requirements", "public access rights"]
        )
    
    async def _run_topic_analysis(
        self, 
        pipeline_id: str, 
        request: ArticleRequest,
        competitor_insights: Optional[CompetitorInsights]
    ) -> TopicRecommendation:
        """Run topic analysis agent"""
        pipeline_logger.log(pipeline_id, 'info', "Analyzing topic opportunities...")
        
        # Use provided topic or generate from insights
        if request.topic:
            topic = request.topic
            keywords = request.keywords or []
        else:
            # Generate from competitor insights
            topic = competitor_insights.content_gaps[0] if competitor_insights else "Service Dog Training Guide"
            keywords = competitor_insights.recommended_keywords[:5] if competitor_insights else []
        
        return TopicRecommendation(
            topic=topic,
            primary_keyword=keywords[0] if keywords else topic.lower(),
            secondary_keywords=keywords[1:] if len(keywords) > 1 else [],
            search_volume=1000,
            competition_level="medium",
            content_type="guide"
        )
    
    async def _run_article_generation(self, pipeline_id: str, topic: TopicRecommendation) -> ArticleModel:
        """Run article generation agent"""
        pipeline_logger.log(pipeline_id, 'info', f"Generating article for: {topic.topic}")
        
        # TODO: Implement real Claude API call
        # For now, generate mock article
        content = f"""# {topic.topic}

This is a comprehensive guide about {topic.topic}.

## Introduction

{topic.topic} is an important topic for service dog handlers and those interested in understanding ADA requirements.

## Key Points

1. Understanding the basics
2. Legal requirements
3. Best practices
4. Common misconceptions

## Conclusion

For more information about {topic.topic}, consult with qualified professionals and refer to official ADA guidelines.
"""
        
        return ArticleModel(
            title=topic.topic,
            slug=topic.topic.lower().replace(' ', '-'),
            content_markdown=content,
            content_html=f"<h1>{topic.topic}</h1><p>Article content here...</p>",
            excerpt=f"Learn everything about {topic.topic} in this comprehensive guide.",
            meta_title=f"{topic.topic} - Complete Guide 2024",
            meta_description=f"Discover everything you need to know about {topic.topic}. Expert insights and practical tips.",
            primary_keyword=topic.primary_keyword,
            secondary_keywords=topic.secondary_keywords,
            word_count=len(content.split()),
            reading_time=max(1, len(content.split()) // 200),
            seo_score=0.85
        )
    
    async def _run_fact_checking(self, pipeline_id: str, article: ArticleModel) -> FactCheckReport:
        """Run legal fact checking agent"""
        pipeline_logger.log(pipeline_id, 'info', "Running fact check...")
        
        # Mock fact checking - implement real checking later
        return FactCheckReport(
            is_approved=True,
            accuracy_score=0.95,
            issues_found=[],
            suggestions=[],
            legal_citations_verified=True
        )
    
    async def _run_wordpress_publishing(self, pipeline_id: str, article: ArticleModel) -> WordPressResult:
        """Publish article to WordPress"""
        pipeline_logger.log(pipeline_id, 'info', "Publishing to WordPress...")
        
        try:
            result = await self.wp_publisher.create_post(
                title=article.title,
                content=article.content_html,
                status='draft',  # Always draft for safety
                slug=article.slug,
                meta={
                    'meta_title': article.meta_title,
                    'meta_description': article.meta_description
                }
            )
            
            if result['success']:
                return WordPressResult(
                    success=True,
                    post_id=result['post_id'],
                    post_url=result['link'],
                    edit_url=result['edit_link']
                )
            else:
                return WordPressResult(
                    success=False,
                    error=result.get('error', 'Unknown error')
                )
                
        except Exception as e:
            logger.error(f"WordPress publishing failed: {e}")
            return WordPressResult(
                success=False,
                error=str(e)
            )
    
    def get_pipeline_history(self, limit: int = 20) -> List[PipelineResult]:
        """Get pipeline history from database"""
        try:
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                pipelines = pipeline_repo.get_recent(limit)
                
                # Convert to PipelineResult objects
                results = []
                for p in pipelines:
                    result = PipelineResult(
                        pipeline_id=p.pipeline_id,
                        status=PipelineStatus(p.status) if p.status else PipelineStatus.PENDING,
                        started_at=p.started_at or datetime.utcnow(),
                        completed_at=p.completed_at,
                        execution_time=p.execution_time_seconds,
                        total_cost=p.total_cost or 0
                    )
                    
                    # Add components if available
                    if p.topic_recommendation:
                        result.topic_recommendation = TopicRecommendation(**p.topic_recommendation)
                    
                    if p.fact_check_report:
                        result.fact_check_report = FactCheckReport(**p.fact_check_report)
                    
                    if p.wordpress_result:
                        result.wordpress_result = WordPressResult(**p.wordpress_result)
                    
                    # Get associated article if exists
                    if p.article:
                        article_data = p.article.to_dict()
                        result.article = ArticleModel(
                            title=article_data['title'],
                            slug=article_data['slug'],
                            content_markdown=article_data['content_markdown'],
                            content_html=article_data.get('content_html', ''),
                            excerpt=article_data.get('excerpt', ''),
                            meta_title=article_data.get('meta_title', ''),
                            meta_description=article_data.get('meta_description', ''),
                            primary_keyword=article_data.get('primary_keyword', ''),
                            secondary_keywords=article_data.get('secondary_keywords', []),
                            word_count=article_data.get('word_count', 0),
                            reading_time=article_data.get('reading_time', 0),
                            seo_score=article_data.get('seo_score', 0)
                        )
                    
                    results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"Failed to get pipeline history: {e}")
            return []
    
    async def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics from database"""
        try:
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                article_repo = ArticleRepository(db)
                
                # Get cost stats
                cost_stats = pipeline_repo.get_cost_stats(days=30)
                
                # Get article stats
                article_stats = article_repo.get_stats()
                
                # Get active pipelines
                active = pipeline_repo.get_active()
                
                return {
                    'total_pipelines': cost_stats['pipeline_count'],
                    'active_pipelines': len(active),
                    'total_articles': article_stats['total'],
                    'published_articles': article_stats['published'],
                    'draft_articles': article_stats['draft'],
                    'total_cost_30d': cost_stats['total_cost'],
                    'avg_cost_per_article': cost_stats['avg_cost_per_pipeline'],
                    'articles_last_30d': article_stats['recent_30_days']
                }
                
        except Exception as e:
            logger.error(f"Failed to get pipeline stats: {e}")
            return {
                'total_pipelines': 0,
                'active_pipelines': 0,
                'total_articles': 0,
                'published_articles': 0,
                'draft_articles': 0,
                'total_cost_30d': 0,
                'avg_cost_per_article': 0,
                'articles_last_30d': 0
            }
    
    async def get_active_pipelines(self) -> List[Dict[str, Any]]:
        """Get currently active pipelines"""
        try:
            with get_db_session() as db:
                pipeline_repo = PipelineRepository(db)
                active = pipeline_repo.get_active()
                
                return [
                    {
                        'pipeline_id': p.pipeline_id,
                        'status': p.status,
                        'started_at': p.started_at.isoformat() if p.started_at else None,
                        'current_stage': 'Processing...'
                    }
                    for p in active
                ]
                
        except Exception as e:
            logger.error(f"Failed to get active pipelines: {e}")
            return []