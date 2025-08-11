"""
Orchestration Manager for Multi-Agent Blog Generation Pipeline

Coordinates the sequential execution of all agents:
1. Competitor Monitoring Agent - Tracks industry content
2. Topic Analysis Agent - Identifies SEO opportunities
3. Article Generation Agent - Creates content
4. Legal Fact Checker Agent - Verifies ADA compliance
5. WordPress Publishing Agent - Deploys content
"""
import asyncio
import json
import logging
import hashlib
import uuid
import glob
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field
from enum import Enum

# Import all agents
from agents.competitor_monitoring_agent import CompetitorMonitoringAgent, CompetitorInsights
from agents.topic_analysis_agent import TopicAnalysisAgent, TopicRecommendation
from agents.article_generation_agent import ArticleGenerationAgent, GeneratedArticle, SEORequirements
from agents.legal_fact_checker_agent import LegalFactCheckerAgent, LegalFactCheckReport
from .wordpress_publisher import WordPressPublisher
from .vector_search import VectorSearchManager
from .pipeline_logger import pipeline_logger, LogLevel

logger = logging.getLogger(__name__)


class PipelineStatus(str, Enum):
    """Status of the pipeline execution"""
    PENDING = "pending"
    MONITORING = "monitoring_competitors"
    ANALYZING = "analyzing_topics"
    GENERATING = "generating_article"
    FACT_CHECKING = "fact_checking"
    PUBLISHING = "publishing"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelineConfig(BaseModel):
    """Configuration for the orchestration pipeline"""
    # Topic configuration
    topic: Optional[str] = None
    primary_keyword: Optional[str] = None
    secondary_keywords: List[str] = Field(default_factory=list)
    
    # Content requirements
    min_words: int = 1500
    max_words: int = 2500
    brand_voice: str = "professional, empathetic, and informative"
    target_audience: str = "Service dog handlers and business owners"
    
    # Publishing settings
    publish_status: str = "draft"  # draft or publish
    wordpress_categories: List[int] = Field(default_factory=list)
    wordpress_tags: List[int] = Field(default_factory=list)
    
    # Feature flags
    use_competitor_insights: bool = True
    perform_fact_checking: bool = True
    auto_publish: bool = False
    
    # Budget controls
    max_cost_per_article: float = 0.50
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 5  # seconds


class PipelineResult(BaseModel):
    """Result of the pipeline execution"""
    status: PipelineStatus
    article: Optional[GeneratedArticle] = None
    fact_check_report: Optional[LegalFactCheckReport] = None
    wordpress_result: Optional[Dict[str, Any]] = None
    competitor_insights: Optional[Dict[str, Any]] = None
    topic_recommendation: Optional[TopicRecommendation] = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    total_cost: float = 0.0
    execution_time: float = 0.0
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class OrchestrationManager:
    """
    Manages the coordination of all agents in the blog generation pipeline
    """
    
    def __init__(self):
        """Initialize the orchestration manager with all agents"""
        self.competitor_agent = CompetitorMonitoringAgent()
        self.topic_agent = TopicAnalysisAgent()
        self.article_agent = ArticleGenerationAgent()
        self.legal_checker = LegalFactCheckerAgent()
        self.wp_publisher = WordPressPublisher()
        self.vector_search = VectorSearchManager()
        
        self.current_pipeline: Optional[PipelineResult] = None
        self.pipeline_history: List[PipelineResult] = []
        self.current_status: Optional[PipelineStatus] = None
        
        # Dashboard metrics
        self.articles_today = 0
        self.articles_this_week = 0
        self.articles_this_month = 0
        self.total_cost_today = 0.0
        self.total_cost_this_month = 0.0
        self.average_generation_time = 0.0
        self.success_rate = 100.0
        self.last_error: Optional[str] = None
        
        # Load pipeline history from saved files
        self._load_pipeline_history()
    
    async def run_pipeline(self, config: PipelineConfig) -> PipelineResult:
        """
        Execute the complete multi-agent pipeline
        
        Args:
            config: Pipeline configuration
            
        Returns:
            PipelineResult with execution details
        """
        start_time = datetime.now()
        result = PipelineResult(status=PipelineStatus.PENDING)
        
        try:
            # Store current pipeline
            self.current_pipeline = result
            
            # Step 1: Competitor Monitoring (if enabled)
            competitor_insights = None
            if config.use_competitor_insights:
                result.status = PipelineStatus.MONITORING
                self.current_status = PipelineStatus.MONITORING
                logger.info("Step 1: Monitoring competitors...")
                competitor_insights = await self._run_competitor_monitoring()
                result.competitor_insights = competitor_insights
            
            # Step 2: Topic Analysis
            result.status = PipelineStatus.ANALYZING
            self.current_status = PipelineStatus.ANALYZING
            logger.info("Step 2: Analyzing topics and SEO opportunities...")
            topic_rec = await self._analyze_topics(
                competitor_insights,
                config.topic,
                config.primary_keyword
            )
            result.topic_recommendation = topic_rec
            
            # Use recommended topic if none provided
            if not config.topic and topic_rec:
                config.topic = topic_rec.title
                config.primary_keyword = topic_rec.primary_keyword
                config.secondary_keywords = topic_rec.secondary_keywords
                logger.info(f"Selected topic from analysis: {config.topic}")
            
            # Step 3: Article Generation
            result.status = PipelineStatus.GENERATING
            self.current_status = PipelineStatus.GENERATING
            logger.info(f"Step 3: Generating article about '{config.topic}'...")
            
            # Get internal links from vector search
            internal_links = await self._get_internal_links(config.topic)
            
            # Generate article with internal links
            article = await self._generate_article(config, competitor_insights, internal_links)
            result.article = article
            result.total_cost += article.cost_tracking.cost if article.cost_tracking else 0
            
            # Index the new article in vector search
            if article:
                await self._index_article(article)
            
            # Step 4: Legal Fact Checking (if enabled)
            if config.perform_fact_checking and article:
                result.status = PipelineStatus.FACT_CHECKING
                logger.info("Step 4: Performing legal fact checking...")
                fact_report = await self._check_legal_facts(article)
                result.fact_check_report = fact_report
                
                # Apply corrections if needed
                if fact_report.incorrect_claims > 0:
                    article = await self._apply_fact_corrections(article, fact_report)
                    result.article = article
            
            # Step 5: WordPress Publishing (if enabled)
            if config.auto_publish and article:
                result.status = PipelineStatus.PUBLISHING
                logger.info("Step 5: Publishing to WordPress...")
                wp_result = await self._publish_to_wordpress(article, config)
                result.wordpress_result = wp_result
            
            # Mark as completed
            result.status = PipelineStatus.COMPLETED
            self.current_status = None  # Clear current status when completed
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - start_time).total_seconds()
            
            logger.info(f"Pipeline completed successfully in {result.execution_time:.2f} seconds")
            logger.info(f"Total cost: ${result.total_cost:.4f}")
            
            # Store in history
            self.pipeline_history.append(result)
            
        except Exception as e:
            result.status = PipelineStatus.FAILED
            self.current_status = None  # Clear current status when failed
            result.errors.append(str(e))
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - start_time).total_seconds()
            
            logger.error(f"Pipeline failed: {e}")
            self.pipeline_history.append(result)
            raise
        
        finally:
            self.current_pipeline = None
        
        return result
    
    async def _run_competitor_monitoring(self) -> Dict[str, Any]:
        """Run competitor monitoring and return insights"""
        try:
            # Scan competitors
            content = await self.competitor_agent.scan_competitors()
            
            # Generate insights
            insights = await self.competitor_agent.generate_insights()
            
            return {
                "content_pieces": len(content),
                "trending_topics": [
                    {"topic": t.topic, "score": t.trend_score}
                    for t in insights.trending_topics[:5]
                ],
                "content_gaps": [
                    {"topic": g.topic, "opportunity": g.opportunity_score}
                    for g in insights.content_gaps[:5]
                ],
                "recommended_topics": insights.recommended_topics[:5]
            }
        except Exception as e:
            logger.warning(f"Competitor monitoring failed: {e}")
            return {}
    
    async def _analyze_topics(
        self,
        competitor_insights: Optional[Dict[str, Any]],
        existing_topic: Optional[str],
        primary_keyword: Optional[str]
    ) -> Optional[TopicRecommendation]:
        """Analyze topics and get recommendations"""
        try:
            # If we already have a topic, skip analysis
            if existing_topic:
                logger.info(f"Using provided topic: {existing_topic}")
                return None
            
            # Get competitor content for gap analysis
            competitor_content = []
            if competitor_insights:
                # Extract competitor topics
                for topic_data in competitor_insights.get("trending_topics", []):
                    competitor_content.append({"title": topic_data.get("topic", "")})
            
            # Prepare keywords for analysis
            keywords = []
            if primary_keyword:
                keywords.append(primary_keyword)
            if competitor_insights:
                # Add trending topics as keywords
                for topic_data in competitor_insights.get("trending_topics", [])[:3]:
                    keywords.append(topic_data.get("topic", ""))
            
            # If no keywords, use quick recommendations
            if not keywords:
                logger.info("Getting quick topic recommendations...")
                recommendations = await self.topic_agent.get_quick_recommendations(count=1)
                return recommendations[0] if recommendations else None
            
            # Perform topic analysis
            logger.info(f"Analyzing {len(keywords)} keywords for opportunities...")
            analysis_report = await self.topic_agent.analyze_topics(
                competitor_content=competitor_content,
                target_keywords=keywords,
                max_recommendations=3
            )
            
            # Log insights
            logger.info(
                f"Topic analysis complete: {analysis_report.content_gaps_found} gaps found, "
                f"{analysis_report.topics_recommended} topics recommended"
            )
            
            # Return top recommendation
            if analysis_report.recommendations:
                top_rec = analysis_report.recommendations[0]
                logger.info(
                    f"Top recommendation: {top_rec.title} "
                    f"(Priority: {top_rec.priority_score:.1f}/100)"
                )
                return top_rec
            
            return None
            
        except Exception as e:
            logger.warning(f"Topic analysis failed: {e}")
            return None
    
    async def _get_internal_links(self, topic: str) -> List[Dict[str, Any]]:
        """Get internal link recommendations from vector search"""
        try:
            links = await self.vector_search.get_internal_links(
                content=topic,
                limit=5,
                min_similarity=0.6
            )
            logger.info(f"Found {len(links)} internal link recommendations")
            return links
        except Exception as e:
            logger.warning(f"Failed to get internal links: {e}")
            return []
    
    async def _index_article(self, article: GeneratedArticle) -> bool:
        """Index the generated article in vector search"""
        try:
            # Combine title and content for indexing
            full_content = f"{article.title}\n\n{article.content_markdown}"
            
            # Index in articles collection
            success = await self.vector_search.index_document(
                content=full_content,
                document_id=article.slug or hashlib.md5(article.title.encode()).hexdigest(),
                title=article.title,
                url=f"/articles/{article.slug}",
                metadata={
                    "primary_keyword": article.primary_keyword,
                    "secondary_keywords": article.secondary_keywords,
                    "seo_score": article.seo_score,
                    "word_count": article.word_count,
                    "generated_at": datetime.now().isoformat()
                },
                collection=self.vector_search.ARTICLES_COLLECTION
            )
            
            if success:
                logger.info(f"Article indexed in vector search: {article.title}")
            else:
                logger.warning(f"Failed to index article: {article.title}")
            
            return success
        except Exception as e:
            logger.error(f"Error indexing article: {e}")
            return False
    
    async def _generate_article(
        self, 
        config: PipelineConfig, 
        competitor_insights: Optional[Dict[str, Any]],
        internal_links: Optional[List[Dict[str, Any]]] = None
    ) -> GeneratedArticle:
        """Generate article using the article generation agent"""
        # Create SEO requirements
        seo_reqs = SEORequirements(
            primary_keyword=config.primary_keyword or "service dogs",
            secondary_keywords=config.secondary_keywords[:5],
            min_words=config.min_words,
            max_words=config.max_words,
            internal_links_count=3,
            external_links_count=2
        )
        
        # Generate article
        article = await self.article_agent.generate_article(
            topic=config.topic,
            seo_requirements=seo_reqs,
            brand_voice=config.brand_voice,
            target_audience=config.target_audience,
            competitor_insights=competitor_insights
        )
        
        # Check cost
        if article.cost_tracking and article.cost_tracking.cost > config.max_cost_per_article:
            logger.warning(
                f"Article cost ${article.cost_tracking.cost:.4f} exceeds limit "
                f"${config.max_cost_per_article:.4f}"
            )
        
        return article
    
    async def _check_legal_facts(self, article: GeneratedArticle) -> LegalFactCheckReport:
        """Check article for legal accuracy"""
        # Combine title and content for checking
        full_content = f"{article.title}\n\n{article.content_markdown}"
        
        # Perform fact checking
        report = await self.legal_checker.fact_check_article(
            article_content=full_content,
            article_title=article.title,
            check_citations=True,
            check_claims=True,
            suggest_corrections=True
        )
        
        # Log results
        logger.info(
            f"Fact check complete: {report.verified_claims}/{report.total_claims} verified, "
            f"{report.incorrect_claims} incorrect, accuracy: {report.overall_accuracy_score:.1%}"
        )
        
        # Add warnings if accuracy is low
        if report.overall_accuracy_score < 0.8:
            logger.warning(f"Low accuracy score: {report.overall_accuracy_score:.1%}")
        
        return report
    
    async def _apply_fact_corrections(
        self, 
        article: GeneratedArticle, 
        fact_report: LegalFactCheckReport
    ) -> GeneratedArticle:
        """Apply fact corrections to the article"""
        content = article.content_markdown
        
        # Apply suggested corrections
        for correction in fact_report.suggested_corrections:
            original = correction.get("original", "")
            corrected = correction.get("corrected", "")
            
            if original and corrected and original in content:
                content = content.replace(original, corrected)
                logger.info(f"Applied correction: '{original[:50]}...' -> '{corrected[:50]}...'")
        
        # Add required disclaimers
        if fact_report.required_disclaimers:
            disclaimer_section = "\n\n## Important Disclaimers\n\n"
            for disclaimer in fact_report.required_disclaimers:
                disclaimer_section += f"- {disclaimer}\n"
            content += disclaimer_section
            logger.info(f"Added {len(fact_report.required_disclaimers)} disclaimers")
        
        # Update article
        article.content_markdown = content
        article.content_html = content  # Would need proper markdown->HTML conversion
        
        return article
    
    async def _publish_to_wordpress(
        self, 
        article: GeneratedArticle, 
        config: PipelineConfig
    ) -> Dict[str, Any]:
        """Publish article to WordPress"""
        # Test connection first
        connected = await self.wp_publisher.test_connection()
        if not connected:
            raise Exception("Failed to connect to WordPress")
        
        # Create the post
        result = await self.wp_publisher.create_post(
            title=article.title,
            content=article.content_html,
            status=config.publish_status,
            slug=article.slug,
            categories=config.wordpress_categories,
            tags=config.wordpress_tags,
            meta={
                "meta_title": article.meta_title,
                "meta_description": article.meta_description
            }
        )
        
        if result["success"]:
            logger.info(f"Published to WordPress: {result['edit_link']}")
        else:
            logger.error(f"WordPress publishing failed: {result.get('error')}")
        
        return result
    
    def get_pipeline_status(self) -> Optional[PipelineStatus]:
        """Get current pipeline status"""
        if self.current_pipeline:
            return self.current_pipeline.status
        return None
    
    def get_pipeline_history(self, limit: int = 10) -> List[PipelineResult]:
        """Get recent pipeline execution history"""
        return self.pipeline_history[-limit:]
    
    def get_cost_summary(self) -> Dict[str, float]:
        """Get cost summary across all executions"""
        total_cost = sum(p.total_cost for p in self.pipeline_history)
        avg_cost = total_cost / len(self.pipeline_history) if self.pipeline_history else 0
        
        return {
            "total_cost": total_cost,
            "average_cost": avg_cost,
            "executions": len(self.pipeline_history)
        }
    
    async def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get comprehensive pipeline statistics for dashboard"""
        successful_runs = len([r for r in self.pipeline_history if r.status == PipelineStatus.COMPLETED])
        failed_runs = len([r for r in self.pipeline_history if r.status == PipelineStatus.FAILED])
        
        cost_summary = self.get_cost_summary()
        
        return {
            "total_runs": len(self.pipeline_history),
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "success_rate": (successful_runs / len(self.pipeline_history)) * 100 if self.pipeline_history else 0,
            "total_cost": cost_summary["total_cost"],
            "average_cost": cost_summary["average_cost"],
            "last_run": self.pipeline_history[-1].started_at.isoformat() if self.pipeline_history else None,
            "current_status": self.current_status.value if self.current_status else "idle",
            "recent_activities": self._get_recent_activities(),
            "articles_generated": len([r for r in self.pipeline_history if r.generated_article]),
            "articles_published": len([r for r in self.pipeline_history if r.wordpress_result]),
            "facts_checked": len([r for r in self.pipeline_history if r.fact_check_report]),
            "topics_analyzed": len(self.pipeline_history),
            "last_competitor_scan": "2025-01-10 18:00:00"  # Placeholder
        }
    
    def _get_recent_activities(self) -> List[Dict[str, Any]]:
        """Get recent pipeline activities for dashboard"""
        activities = []
        
        for result in self.pipeline_history[-5:]:  # Last 5 activities
            activities.append({
                "action": f"Pipeline {result.status.value}",
                "details": f"Topic: {result.topic or 'Auto-generated'}",
                "timestamp": result.started_at.strftime("%H:%M:%S"),
                "status": result.status.value
            })
        
        return list(reversed(activities))  # Most recent first
    
    async def get_active_pipelines(self) -> List[Dict[str, Any]]:
        """Get currently running pipelines"""
        if self.current_status and self.current_status != PipelineStatus.COMPLETED:
            return [{
                "pipeline_id": "current_pipeline",
                "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "primary_keyword": "service dog training",  # Placeholder
                "status": "running",
                "progress": self._get_progress_percentage(),
                "eta": "2 minutes",
                "steps": self._get_current_steps()
            }]
        return []
    
    def _get_progress_percentage(self) -> int:
        """Calculate progress percentage based on current status"""
        progress_map = {
            PipelineStatus.PENDING: 0,
            PipelineStatus.MONITORING: 20,
            PipelineStatus.ANALYZING: 40,
            PipelineStatus.GENERATING: 60,
            PipelineStatus.FACT_CHECKING: 80,
            PipelineStatus.PUBLISHING: 90,
            PipelineStatus.COMPLETED: 100,
            PipelineStatus.FAILED: 100
        }
        return progress_map.get(self.current_status, 0)
    
    def _get_current_steps(self) -> List[Dict[str, Any]]:
        """Get current pipeline steps with status"""
        steps = [
            {"name": "Competitor Monitoring", "status": "completed"},
            {"name": "Topic Analysis", "status": "completed"},
            {"name": "Article Generation", "status": "running" if self.current_status == PipelineStatus.GENERATING else "completed"},
            {"name": "Legal Fact Checking", "status": "pending"},
            {"name": "WordPress Publishing", "status": "pending"}
        ]
        return steps
        
    async def get_pipeline_history_dashboard(self) -> List[Dict[str, Any]]:
        """Get pipeline execution history for dashboard"""
        history = []
        
        for i, result in enumerate(self.pipeline_history[-20:]):  # Last 20 runs
            # Generate a unique pipeline ID based on index and timestamp
            pipeline_id = f"pipeline_{result.started_at.strftime('%Y%m%d%H%M%S')}_{i}"
            
            # Extract the primary keyword from topic recommendation or use a default
            primary_keyword = "Unknown"
            if result.topic_recommendation and hasattr(result.topic_recommendation, 'primary_keyword'):
                primary_keyword = result.topic_recommendation.primary_keyword
            elif result.topic_recommendation and hasattr(result.topic_recommendation, 'topic'):
                primary_keyword = result.topic_recommendation.topic
            
            history.append({
                "pipeline_id": pipeline_id,
                "primary_keyword": primary_keyword,
                "started_at": result.started_at.strftime("%Y-%m-%d %H:%M:%S"),
                "time_ago": self._time_ago(result.started_at),
                "duration": result.execution_time if result.execution_time else None,
                "status": result.status.value,
                "cost": result.total_cost,
                "article_generated": bool(result.article),
                "article_id": pipeline_id if result.article else None
            })
        
        return list(reversed(history))  # Most recent first
    
    def _time_ago(self, timestamp: datetime) -> str:
        """Convert timestamp to human readable 'time ago' format"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"
    
    def _load_pipeline_history(self):
        """Load pipeline history from saved article files"""
        try:
            # Find all article files
            article_dir = Path("data/articles")
            if not article_dir.exists():
                logger.info("No article directory found, starting with empty history")
                return
            
            article_files = sorted(article_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
            logger.info(f"Found {len(article_files)} article files")
            
            for article_file in article_files[:50]:  # Load last 50 articles
                try:
                    with open(article_file, 'r') as f:
                        article_data = json.load(f)
                    
                    # Skip invalid files
                    if not article_data.get('generated_at') or not article_data.get('title'):
                        continue
                    
                    # Parse timestamp
                    try:
                        generated_at = datetime.fromisoformat(article_data['generated_at'])
                    except:
                        # Try parsing filename timestamp as fallback
                        filename = article_file.stem
                        if '_' in filename:
                            date_part = filename.split('_')[-1]
                            if len(date_part) == 8:  # YYYYMMDD format
                                generated_at = datetime.strptime(date_part, '%Y%m%d')
                            else:
                                generated_at = datetime.fromtimestamp(article_file.stat().st_mtime)
                        else:
                            generated_at = datetime.fromtimestamp(article_file.stat().st_mtime)
                    
                    # Create a PipelineResult from the article data
                    pipeline_result = PipelineResult(
                        status=PipelineStatus.COMPLETED,  # Assume completed if article exists
                        started_at=generated_at,
                        completed_at=generated_at,
                        execution_time=0.0,  # Unknown
                        total_cost=article_data.get('cost_tracking', {}).get('cost', 0.0),
                        errors=[],
                        warnings=[]
                    )
                    
                    # Create a simplified GeneratedArticle object
                    article = GeneratedArticle(
                        title=article_data.get('title', 'Unknown'),
                        slug=article_data.get('slug', ''),
                        content_markdown=article_data.get('content_markdown', ''),
                        meta_title=article_data.get('meta_title', ''),
                        meta_description=article_data.get('meta_description', ''),
                        primary_keyword=article_data.get('primary_keyword', ''),
                        secondary_keywords=article_data.get('secondary_keywords', []),
                        word_count=article_data.get('word_count', 0),
                        seo_score=article_data.get('seo_score', 0.0),
                        estimated_reading_time=article_data.get('estimated_reading_time', 0),
                        cost_tracking=article_data.get('cost_tracking')
                    )
                    
                    pipeline_result.article = article
                    
                    # Create a topic recommendation if we have keyword data
                    if article_data.get('primary_keyword'):
                        topic_rec = TopicRecommendation(
                            title=article_data.get('title', 'Unknown'),
                            slug=article_data.get('slug', ''),
                            primary_keyword=article_data.get('primary_keyword', ''),
                            secondary_keywords=article_data.get('secondary_keywords', []),
                            content_type="article",
                            target_word_count=article_data.get('word_count', 1500),
                            priority_score=85.0,
                            rationale="Reconstructed from saved article",
                            content_outline=["Introduction", "Main Content", "Conclusion"]
                        )
                        pipeline_result.topic_recommendation = topic_rec
                    
                    self.pipeline_history.append(pipeline_result)
                    
                except Exception as e:
                    logger.warning(f"Could not load article {article_file}: {e}")
                    continue
            
            # Sort by started_at
            self.pipeline_history.sort(key=lambda x: x.started_at, reverse=True)
            logger.info(f"Loaded {len(self.pipeline_history)} pipeline results from saved articles")
            
        except Exception as e:
            logger.error(f"Failed to load pipeline history: {e}")
            self.pipeline_history = []

    async def close(self):
        """Clean up resources"""
        await self.competitor_agent.close()


# Example usage
async def main():
    """Example of running the full pipeline"""
    manager = OrchestrationManager()
    
    # Configure pipeline
    config = PipelineConfig(
        topic="How to Train a Service Dog for PTSD Support",
        primary_keyword="PTSD service dog",
        secondary_keywords=["service dog training", "PTSD support", "ADA requirements"],
        use_competitor_insights=True,
        perform_fact_checking=True,
        auto_publish=False,  # Keep as draft
        publish_status="draft"
    )
    
    # Run pipeline
    result = await manager.run_pipeline(config)
    
    # Display results
    print(f"\n📊 Pipeline Results")
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f} seconds")
    print(f"Total Cost: ${result.total_cost:.4f}")
    
    if result.article:
        print(f"\n📝 Generated Article:")
        print(f"Title: {result.article.title}")
        print(f"Word Count: {result.article.word_count}")
        print(f"SEO Score: {result.article.seo_score}/100")
    
    if result.fact_check_report:
        print(f"\n✅ Fact Check Report:")
        print(f"Accuracy: {result.fact_check_report.overall_accuracy_score:.1%}")
        print(f"Verified Claims: {result.fact_check_report.verified_claims}")
        print(f"Incorrect Claims: {result.fact_check_report.incorrect_claims}")
    
    if result.wordpress_result and result.wordpress_result.get("success"):
        print(f"\n🌐 WordPress Publishing:")
        print(f"Post ID: {result.wordpress_result['post_id']}")
        print(f"Edit Link: {result.wordpress_result['edit_link']}")
    
    await manager.close()


if __name__ == "__main__":
    asyncio.run(main())