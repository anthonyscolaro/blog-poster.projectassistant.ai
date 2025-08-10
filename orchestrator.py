"""
Workflow Orchestrator for Blog Automation System
Lightweight implementation using FastAPI + Redis for MVP
"""
import asyncio
import json
import redis.asyncio as redis
from uuid import uuid4
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)


class WorkflowState(str, Enum):
    PENDING = "pending"
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    FACT_CHECKING = "fact_checking"
    AWAITING_APPROVAL = "awaiting_approval"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    COMPENSATING = "compensating"


class WorkflowStep(BaseModel):
    """Individual workflow step with retry logic"""
    name: str
    agent: str
    max_retries: int = 3
    retry_delay_seconds: int = 60
    timeout_seconds: int = 300
    requires_approval: bool = False
    compensation_action: Optional[str] = None


class WorkflowDAG(BaseModel):
    """Complete workflow definition"""
    workflow_id: str
    created_at: datetime
    state: WorkflowState = WorkflowState.PENDING
    current_step: Optional[str] = None
    steps_completed: List[str] = Field(default_factory=list)
    retry_count: Dict[str, int] = Field(default_factory=dict)
    
    steps: List[WorkflowStep] = [
        WorkflowStep(
            name="monitor_competitors",
            agent="competitor_monitoring",
            max_retries=5,
            retry_delay_seconds=300
        ),
        WorkflowStep(
            name="analyze_topics", 
            agent="topic_analysis",
            max_retries=3
        ),
        WorkflowStep(
            name="generate_article",
            agent="article_generation",
            max_retries=2,
            timeout_seconds=600
        ),
        WorkflowStep(
            name="fact_check",
            agent="legal_fact_checker",
            max_retries=1,
            requires_approval=True
        ),
        WorkflowStep(
            name="publish_to_wordpress",
            agent="wordpress_publishing",
            max_retries=3,
            compensation_action="delete_wp_draft"
        )
    ]
    
    error_log: List[Dict[str, Any]] = Field(default_factory=list)
    approval_requests: List[Dict[str, Any]] = Field(default_factory=list)
    articles_generated: List[str] = Field(default_factory=list)
    total_cost: float = 0.0


class ApprovalRequest(BaseModel):
    """Human approval request"""
    request_id: str
    workflow_id: str
    step_name: str
    article_data: Dict[str, Any]
    created_at: datetime
    expires_at: datetime
    approval_url: HttpUrl


class WorkflowMetrics(BaseModel):
    """Workflow execution metrics"""
    workflow_id: str
    total_duration_seconds: float
    step_durations: Dict[str, float]
    api_costs: Dict[str, float]
    tokens_used: Dict[str, int]
    retry_attempts: Dict[str, int]
    approval_wait_time_hours: Optional[float] = None


class WorkflowOrchestrator:
    """Orchestrates the blog automation workflow"""
    
    def __init__(self, redis_url: str = "redis://localhost:6380"):
        self.redis = None
        self.redis_url = redis_url
        self.scheduler = AsyncIOScheduler()
        self.article_count = 0  # Track articles for approval gate
        
    async def connect(self):
        """Initialize Redis connection"""
        self.redis = await redis.from_url(self.redis_url)
        
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
    
    async def create_workflow(self) -> WorkflowDAG:
        """Create a new workflow instance"""
        workflow = WorkflowDAG(
            workflow_id=str(uuid4()),
            created_at=datetime.utcnow()
        )
        
        # Store in Redis
        await self.redis.setex(
            f"workflow:{workflow.workflow_id}",
            86400,  # 24 hour TTL
            workflow.json()
        )
        
        return workflow
    
    async def execute_workflow(self, workflow_id: str):
        """Execute the complete workflow"""
        workflow = await self.get_workflow(workflow_id)
        
        try:
            for step in workflow.steps:
                workflow.current_step = step.name
                workflow.state = self._get_state_for_step(step.name)
                await self.save_workflow(workflow)
                
                # Execute step with retries
                result = await self.execute_with_retry(workflow, step)
                
                # Handle approval gate
                if step.requires_approval and self.article_count < 10:
                    workflow.state = WorkflowState.AWAITING_APPROVAL
                    await self.save_workflow(workflow)
                    
                    approval = await self.request_approval(workflow, result)
                    if not approval:
                        raise Exception("Article rejected by reviewer")
                
                workflow.steps_completed.append(step.name)
                await self.save_workflow(workflow)
                
            workflow.state = WorkflowState.PUBLISHED
            await self.save_workflow(workflow)
            
        except Exception as e:
            workflow.state = WorkflowState.FAILED
            workflow.error_log.append({
                "step": workflow.current_step,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
            await self.save_workflow(workflow)
            raise
    
    async def execute_with_retry(self, workflow: WorkflowDAG, step: WorkflowStep) -> Any:
        """Execute step with exponential backoff retry"""
        for attempt in range(step.max_retries):
            try:
                # Simulate agent execution
                result = await self.execute_agent(step.agent, workflow)
                return result
                
            except Exception as e:
                workflow.retry_count[step.name] = attempt + 1
                
                if attempt == step.max_retries - 1:
                    # Final attempt failed, trigger compensation
                    if step.compensation_action:
                        await self.compensate(step.compensation_action, workflow)
                    raise
                    
                # Exponential backoff
                delay = step.retry_delay_seconds * (2 ** attempt)
                logger.warning(f"Step {step.name} failed (attempt {attempt + 1}), retrying in {delay}s")
                await asyncio.sleep(delay)
    
    async def execute_agent(self, agent_name: str, workflow: WorkflowDAG) -> Dict[str, Any]:
        """Execute a specific agent (stubbed for MVP)"""
        logger.info(f"Executing agent: {agent_name}")
        
        # In production, this would call actual agent implementations
        # For MVP, return mock data
        if agent_name == "competitor_monitoring":
            return {"new_content": ["topic1", "topic2"]}
        elif agent_name == "topic_analysis":
            return {"recommended_topic": "ada-service-dog-requirements"}
        elif agent_name == "article_generation":
            self.article_count += 1
            return {
                "title": "Understanding ADA Service Dog Requirements",
                "content": "Article content here...",
                "cost": 0.25
            }
        elif agent_name == "legal_fact_checker":
            return {"verified": True, "confidence": 0.98}
        elif agent_name == "wordpress_publishing":
            return {"post_id": 123, "url": "https://servicedogus.org/article"}
        
        return {}
    
    async def compensate(self, action: str, workflow: WorkflowDAG):
        """Execute compensation action on failure"""
        logger.info(f"Executing compensation: {action}")
        
        if action == "delete_wp_draft":
            # Would call WordPress API to delete draft
            pass
        elif action == "rollback_vectors":
            # Would rollback vector DB transaction
            pass
        elif action == "notify_admin":
            # Would send alert to admin
            pass
    
    async def request_approval(self, workflow: WorkflowDAG, article_data: Dict) -> bool:
        """Request human approval for article"""
        request = ApprovalRequest(
            request_id=str(uuid4()),
            workflow_id=workflow.workflow_id,
            step_name=workflow.current_step,
            article_data=article_data,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(hours=24),
            approval_url=f"https://servicedogus.org/admin/approve/{workflow.workflow_id}"
        )
        
        # Store approval request
        await self.redis.setex(
            f"approval:{request.request_id}",
            86400,
            request.json()
        )
        
        # In production, would send Slack/email notification
        logger.info(f"Approval requested: {request.approval_url}")
        
        # For MVP, auto-approve after delay
        await asyncio.sleep(2)
        return True
    
    async def get_workflow(self, workflow_id: str) -> WorkflowDAG:
        """Retrieve workflow from Redis"""
        data = await self.redis.get(f"workflow:{workflow_id}")
        if not data:
            raise ValueError(f"Workflow {workflow_id} not found")
        return WorkflowDAG.parse_raw(data)
    
    async def save_workflow(self, workflow: WorkflowDAG):
        """Save workflow to Redis"""
        await self.redis.setex(
            f"workflow:{workflow.workflow_id}",
            86400,
            workflow.json()
        )
    
    def _get_state_for_step(self, step_name: str) -> WorkflowState:
        """Map step name to workflow state"""
        state_map = {
            "monitor_competitors": WorkflowState.MONITORING,
            "analyze_topics": WorkflowState.ANALYZING,
            "generate_article": WorkflowState.GENERATING,
            "fact_check": WorkflowState.FACT_CHECKING,
            "publish_to_wordpress": WorkflowState.PUBLISHING
        }
        return state_map.get(step_name, WorkflowState.PENDING)
    
    def setup_schedules(self):
        """Configure scheduled workflow runs"""
        # Competitor monitoring - every 6 hours
        self.scheduler.add_job(
            self.run_scheduled_workflow,
            CronTrigger(hour="*/6"),
            args=["monitoring"],
            id="competitor_monitoring",
            replace_existing=True
        )
        
        # Full workflow - MWF at 9 AM
        self.scheduler.add_job(
            self.run_scheduled_workflow,
            CronTrigger(day_of_week="mon,wed,fri", hour=9),
            args=["full"],
            id="article_generation",
            replace_existing=True
        )
        
        self.scheduler.start()
    
    async def run_scheduled_workflow(self, workflow_type: str):
        """Run a scheduled workflow"""
        workflow = await self.create_workflow()
        logger.info(f"Starting scheduled workflow: {workflow.workflow_id} (type: {workflow_type})")
        
        try:
            await self.execute_workflow(workflow.workflow_id)
            logger.info(f"Workflow completed: {workflow.workflow_id}")
        except Exception as e:
            logger.error(f"Workflow failed: {workflow.workflow_id} - {e}")
    
    async def get_metrics(self, workflow_id: str) -> WorkflowMetrics:
        """Get workflow execution metrics"""
        workflow = await self.get_workflow(workflow_id)
        
        # Calculate metrics
        duration = (datetime.utcnow() - workflow.created_at).total_seconds()
        
        return WorkflowMetrics(
            workflow_id=workflow_id,
            total_duration_seconds=duration,
            step_durations={},  # Would be tracked during execution
            api_costs={"total": workflow.total_cost},
            tokens_used={},  # Would be tracked per agent
            retry_attempts=workflow.retry_count
        )


# FastAPI integration
from fastapi import FastAPI, HTTPException

app = FastAPI()
orchestrator = WorkflowOrchestrator()


@app.on_event("startup")
async def startup():
    await orchestrator.connect()
    orchestrator.setup_schedules()


@app.on_event("shutdown")
async def shutdown():
    await orchestrator.disconnect()


@app.post("/workflow/start")
async def start_workflow():
    """Manually trigger a new workflow"""
    workflow = await orchestrator.create_workflow()
    
    # Run in background
    asyncio.create_task(orchestrator.execute_workflow(workflow.workflow_id))
    
    return {"workflow_id": workflow.workflow_id, "status": "started"}


@app.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    try:
        workflow = await orchestrator.get_workflow(workflow_id)
        return {
            "workflow_id": workflow_id,
            "state": workflow.state,
            "current_step": workflow.current_step,
            "steps_completed": workflow.steps_completed,
            "articles_generated": len(workflow.articles_generated)
        }
    except ValueError:
        raise HTTPException(status_code=404, detail="Workflow not found")


@app.get("/workflow/{workflow_id}/metrics")
async def get_workflow_metrics(workflow_id: str):
    """Get workflow execution metrics"""
    try:
        metrics = await orchestrator.get_metrics(workflow_id)
        return metrics.dict()
    except ValueError:
        raise HTTPException(status_code=404, detail="Workflow not found")


@app.post("/approval/{request_id}")
async def handle_approval(request_id: str, approved: bool = True):
    """Handle human approval response"""
    # Store approval decision
    await orchestrator.redis.set(
        f"approval:response:{request_id}",
        json.dumps({"approved": approved, "timestamp": datetime.utcnow().isoformat()}),
        ex=3600
    )
    
    return {"status": "approved" if approved else "rejected"}