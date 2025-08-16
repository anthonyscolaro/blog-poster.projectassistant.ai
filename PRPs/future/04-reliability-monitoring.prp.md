name: "Reliability, Monitoring & Observability"
description: |

## Purpose
Build comprehensive monitoring, logging, and alerting systems to ensure 99.9% uptime, rapid incident response, and data-driven optimization of the content generation pipeline.

## Core Principles  
1. **Observability First**: Instrument everything, measure what matters
2. **Proactive Monitoring**: Detect issues before users notice
3. **Rapid Recovery**: Automated healing and quick manual intervention
4. **Data-Driven Decisions**: Metrics guide optimization and scaling

---

## Goal
Implement full-stack observability with metrics, logs, traces, health checks, and intelligent alerting to maintain high reliability and performance.

## Why
- **Current Blindness**: No visibility into system health or failures
- **Silent Failures**: Pipelines fail without notification
- **No Performance Data**: Can't optimize without metrics
- **Incident Response**: No way to debug production issues

## What
Complete observability stack with:
- Prometheus metrics collection
- Grafana dashboards
- ELK stack for log aggregation
- Distributed tracing with OpenTelemetry
- Health checks and circuit breakers
- PagerDuty integration for alerts
- Automated recovery procedures

### Success Criteria
- [ ] 99.9% uptime SLA achieved
- [ ] < 5 minute incident detection
- [ ] < 30 minute MTTR (Mean Time To Recovery)
- [ ] 100% critical path instrumented
- [ ] Zero silent failures
- [ ] Automated recovery for 80% of incidents
- [ ] Complete audit trail for all operations
- [ ] Performance baseline established

## All Needed Context

### Monitoring Architecture

```yaml
Components:
  Metrics:
    - Prometheus: Time-series metrics
    - Grafana: Visualization and dashboards
    - AlertManager: Alert routing
    
  Logging:
    - Elasticsearch: Log storage
    - Logstash: Log processing
    - Kibana: Log visualization
    - Filebeat: Log shipping
    
  Tracing:
    - OpenTelemetry: Distributed tracing
    - Jaeger: Trace visualization
    
  Health:
    - Custom health endpoints
    - Dependency checks
    - Circuit breakers
    
  Alerting:
    - PagerDuty: Incident management
    - Slack: Team notifications
    - Email: Backup alerts
```

### Comprehensive Health Checks

```python
# src/monitoring/health.py
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import httpx

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    response_time_ms: float
    metadata: Dict[str, Any] = None

class HealthChecker:
    """Comprehensive health checking system"""
    
    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        checks = await asyncio.gather(
            self.check_database(),
            self.check_redis(),
            self.check_qdrant(),
            self.check_wordpress(),
            self.check_external_apis(),
            self.check_disk_space(),
            self.check_memory(),
            return_exceptions=True
        )
        
        # Aggregate results
        all_healthy = all(
            c.status == HealthStatus.HEALTHY 
            for c in checks 
            if not isinstance(c, Exception)
        )
        
        return {
            'status': 'healthy' if all_healthy else 'unhealthy',
            'checks': [self._serialize_check(c) for c in checks],
            'timestamp': datetime.utcnow().isoformat()
        }
        
    async def check_database(self) -> HealthCheck:
        """Check database connectivity and performance"""
        start = time.time()
        
        try:
            with get_db() as db:
                # Simple query
                result = db.execute("SELECT 1").scalar()
                
                # Check connection pool
                pool_stats = db.bind.pool.status()
                
                response_time = (time.time() - start) * 1000
                
                if response_time > 100:
                    return HealthCheck(
                        name="database",
                        status=HealthStatus.DEGRADED,
                        message="Slow response time",
                        response_time_ms=response_time,
                        metadata={'pool': pool_stats}
                    )
                    
                return HealthCheck(
                    name="database",
                    status=HealthStatus.HEALTHY,
                    message="Connected",
                    response_time_ms=response_time,
                    metadata={'pool': pool_stats}
                )
                
        except Exception as e:
            return HealthCheck(
                name="database",
                status=HealthStatus.UNHEALTHY,
                message=str(e),
                response_time_ms=(time.time() - start) * 1000
            )
            
    async def check_redis(self) -> HealthCheck:
        """Check Redis connectivity"""
        start = time.time()
        
        try:
            redis_client = get_redis()
            await redis_client.ping()
            
            # Check memory usage
            info = await redis_client.info()
            memory_usage = info['used_memory_human']
            
            return HealthCheck(
                name="redis",
                status=HealthStatus.HEALTHY,
                message="Connected",
                response_time_ms=(time.time() - start) * 1000,
                metadata={'memory': memory_usage}
            )
            
        except Exception as e:
            return HealthCheck(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                message=str(e),
                response_time_ms=(time.time() - start) * 1000
            )
            
    async def check_external_apis(self) -> HealthCheck:
        """Check external API availability"""
        apis = {
            'anthropic': 'https://api.anthropic.com/v1/health',
            'jina': 'https://api.jina.ai/health',
            'wordpress': f"{os.getenv('WORDPRESS_URL')}/wp-json"
        }
        
        results = {}
        async with httpx.AsyncClient() as client:
            for name, url in apis.items():
                try:
                    response = await client.get(url, timeout=5.0)
                    results[name] = response.status_code == 200
                except:
                    results[name] = False
                    
        all_healthy = all(results.values())
        
        return HealthCheck(
            name="external_apis",
            status=HealthStatus.HEALTHY if all_healthy else HealthStatus.DEGRADED,
            message="All APIs available" if all_healthy else "Some APIs unavailable",
            response_time_ms=0,
            metadata=results
        )
```

### Metrics Collection

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary
from functools import wraps
import time

# Business Metrics
articles_generated = Counter(
    'articles_generated_total',
    'Total articles generated',
    ['status', 'pipeline_id']
)

article_generation_time = Histogram(
    'article_generation_seconds',
    'Time to generate an article',
    buckets=(5, 10, 30, 60, 120, 300, 600)
)

pipeline_cost = Summary(
    'pipeline_cost_dollars',
    'Cost per pipeline execution'
)

active_pipelines = Gauge(
    'active_pipelines',
    'Currently running pipelines'
)

# System Metrics
api_requests = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_latency = Histogram(
    'api_latency_seconds',
    'API request latency',
    ['method', 'endpoint']
)

database_queries = Counter(
    'database_queries_total',
    'Total database queries',
    ['operation', 'table']
)

cache_hits = Counter(
    'cache_hits_total',
    'Cache hit rate',
    ['cache_type', 'hit']
)

# External Service Metrics
external_api_calls = Counter(
    'external_api_calls_total',
    'External API calls',
    ['service', 'endpoint', 'status']
)

external_api_latency = Histogram(
    'external_api_latency_seconds',
    'External API latency',
    ['service', 'endpoint']
)

# Error Metrics
errors = Counter(
    'errors_total',
    'Total errors',
    ['type', 'severity', 'component']
)

# Decorators
def track_time(metric: Histogram):
    """Decorator to track execution time"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                metric.observe(time.time() - start)
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                metric.observe(time.time() - start)
                
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

def track_errors(component: str):
    """Decorator to track errors"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_type = type(e).__name__
                severity = 'critical' if 'Critical' in error_type else 'error'
                errors.labels(
                    type=error_type,
                    severity=severity,
                    component=component
                ).inc()
                raise
        return wrapper
    return decorator
```

### Structured Logging

```python
# src/monitoring/logging.py
import structlog
from pythonjsonlogger import jsonlogger
import logging.config

# Configure structured logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': jsonlogger.JsonFormatter,
            'format': '%(timestamp)s %(level)s %(name)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/blogposter/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

def get_logger(name: str):
    """Get structured logger"""
    return structlog.get_logger(name)

# Usage example
logger = get_logger(__name__)

class PipelineLogger:
    """Pipeline-specific logging"""
    
    def __init__(self, pipeline_id: str):
        self.logger = get_logger('pipeline')
        self.pipeline_id = pipeline_id
        
    def log(self, event: str, **kwargs):
        """Log pipeline event"""
        self.logger.info(
            event,
            pipeline_id=self.pipeline_id,
            **kwargs
        )
        
    def log_start(self, config: Dict):
        """Log pipeline start"""
        self.log(
            'pipeline_started',
            config=config,
            timestamp=datetime.utcnow().isoformat()
        )
        
    def log_agent_start(self, agent: str):
        """Log agent execution start"""
        self.log(
            'agent_started',
            agent=agent,
            timestamp=datetime.utcnow().isoformat()
        )
        
    def log_agent_complete(self, agent: str, result: Any, duration: float):
        """Log agent completion"""
        self.log(
            'agent_completed',
            agent=agent,
            duration_seconds=duration,
            result_size=len(str(result))
        )
        
    def log_error(self, error: Exception, context: Dict = None):
        """Log pipeline error"""
        self.logger.error(
            'pipeline_error',
            pipeline_id=self.pipeline_id,
            error_type=type(error).__name__,
            error_message=str(error),
            context=context,
            exc_info=True
        )
```

### Distributed Tracing

```python
# src/monitoring/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True
)

# Add span processor
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Auto-instrument libraries
FastAPIInstrumentor.instrument()
HTTPXClientInstrumentor.instrument()
SQLAlchemyInstrumentor.instrument()

def trace_operation(name: str):
    """Decorator for tracing operations"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(name) as span:
                span.set_attribute("function", func.__name__)
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(trace.Status(trace.StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(
                        trace.Status(trace.StatusCode.ERROR, str(e))
                    )
                    span.record_exception(e)
                    raise
                    
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with tracer.start_as_current_span(name) as span:
                span.set_attribute("function", func.__name__)
                try:
                    result = func(*args, **kwargs)
                    span.set_status(trace.Status(trace.StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(
                        trace.Status(trace.StatusCode.ERROR, str(e))
                    )
                    span.record_exception(e)
                    raise
                    
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
```

### Alert Configuration

```yaml
# prometheus/alerts.yml
groups:
  - name: blogposter
    interval: 30s
    rules:
      # High-level alerts
      - alert: PipelineFailureRate
        expr: rate(pipeline_runs_total{status="failed"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
          team: content
        annotations:
          summary: "High pipeline failure rate"
          description: "{{ $value | humanizePercentage }} of pipelines failing"
          
      - alert: ArticleGenerationSlow
        expr: article_generation_seconds > 300
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow article generation"
          description: "Articles taking > 5 minutes to generate"
          
      - alert: BudgetExceeded
        expr: sum(pipeline_cost_dollars) > 400
        labels:
          severity: critical
          team: finance
        annotations:
          summary: "Monthly budget exceeded"
          description: "Spent ${{ $value }} this month"
          
      # System alerts
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage at {{ $value | humanizePercentage }}"
          
      - alert: DatabaseConnectionPoolExhausted
        expr: database_pool_available == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool exhausted"
          
      - alert: ExternalAPIDown
        expr: up{job="external_apis"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "External API {{ $labels.service }} is down"
```

### Grafana Dashboards

```json
{
  "dashboard": {
    "title": "Blog Poster Operations",
    "panels": [
      {
        "title": "Pipeline Success Rate",
        "targets": [
          {
            "expr": "rate(pipeline_runs_total{status='success'}[1h]) / rate(pipeline_runs_total[1h])"
          }
        ]
      },
      {
        "title": "Articles Generated",
        "targets": [
          {
            "expr": "increase(articles_generated_total[1d])"
          }
        ]
      },
      {
        "title": "Average Generation Time",
        "targets": [
          {
            "expr": "rate(article_generation_seconds_sum[1h]) / rate(article_generation_seconds_count[1h])"
          }
        ]
      },
      {
        "title": "Cost per Article",
        "targets": [
          {
            "expr": "pipeline_cost_dollars / articles_generated_total"
          }
        ]
      },
      {
        "title": "API Latency (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, api_latency_seconds_bucket)"
          }
        ]
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(errors_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### Incident Response Automation

```python
# src/monitoring/incident_response.py
from typing import Dict, Any
import asyncio

class IncidentResponder:
    """Automated incident response"""
    
    def __init__(self):
        self.pagerduty = PagerDutyClient()
        self.slack = SlackClient()
        
    async def handle_alert(self, alert: Dict[str, Any]):
        """Handle incoming alert"""
        severity = alert['labels']['severity']
        
        if severity == 'critical':
            await self.handle_critical(alert)
        elif severity == 'warning':
            await self.handle_warning(alert)
            
    async def handle_critical(self, alert: Dict):
        """Handle critical alerts"""
        # Create PagerDuty incident
        incident = await self.pagerduty.create_incident(
            title=alert['annotations']['summary'],
            description=alert['annotations']['description'],
            urgency='high'
        )
        
        # Post to Slack
        await self.slack.post_message(
            channel='#incidents',
            text=f"🚨 CRITICAL: {alert['annotations']['summary']}",
            attachments=[{
                'color': 'danger',
                'fields': [
                    {'title': 'Description', 'value': alert['annotations']['description']},
                    {'title': 'PagerDuty', 'value': incident['html_url']}
                ]
            }]
        )
        
        # Attempt auto-remediation
        await self.auto_remediate(alert)
        
    async def auto_remediate(self, alert: Dict):
        """Attempt automatic remediation"""
        alert_name = alert['alertname']
        
        remediation_map = {
            'DatabaseConnectionPoolExhausted': self.remediate_db_pool,
            'HighMemoryUsage': self.remediate_memory,
            'PipelineStuck': self.remediate_stuck_pipeline
        }
        
        if alert_name in remediation_map:
            await remediation_map[alert_name]()
            
    async def remediate_db_pool(self):
        """Remediate database pool exhaustion"""
        # Kill idle connections
        with get_db() as db:
            db.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE state = 'idle'
                AND state_change < NOW() - INTERVAL '10 minutes'
            """)
            
    async def remediate_memory(self):
        """Remediate high memory usage"""
        # Clear caches
        cache.clear()
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Restart workers if needed
        if get_memory_usage() > 90:
            await restart_celery_workers()
```

### Performance Monitoring

```python
# src/monitoring/performance.py
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class PerformanceMetric:
    name: str
    value: float
    unit: str
    threshold: float
    
class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics = []
        
    async def collect_metrics(self) -> List[PerformanceMetric]:
        """Collect all performance metrics"""
        metrics = []
        
        # API response times
        api_p95 = await self.get_percentile('api_latency_seconds', 95)
        metrics.append(PerformanceMetric(
            name='api_response_p95',
            value=api_p95,
            unit='seconds',
            threshold=1.0
        ))
        
        # Database query times
        db_avg = await self.get_average('database_query_duration')
        metrics.append(PerformanceMetric(
            name='db_query_avg',
            value=db_avg,
            unit='milliseconds',
            threshold=100
        ))
        
        # Article generation time
        gen_avg = await self.get_average('article_generation_seconds')
        metrics.append(PerformanceMetric(
            name='article_generation_avg',
            value=gen_avg,
            unit='seconds',
            threshold=120
        ))
        
        return metrics
        
    def check_sla(self) -> Dict[str, bool]:
        """Check SLA compliance"""
        return {
            'uptime': self.get_uptime() >= 99.9,
            'response_time': self.get_p95_response() <= 1.0,
            'error_rate': self.get_error_rate() <= 0.01
        }
```

---

## Implementation Priority
1. **Week 1**: Basic metrics and health checks
2. **Week 2**: Logging and error tracking
3. **Week 3**: Alerting and incident response
4. **Week 4**: Dashboards and optimization

## Success Metrics
- 99.9% uptime achieved
- < 5 minute alert response time
- 80% of incidents auto-remediated
- Zero undetected failures
- Complete observability coverage