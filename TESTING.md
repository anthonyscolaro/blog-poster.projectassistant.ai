# Blog-Poster Testing Guide

This guide explains how to test the Blog-Poster microSaaS platform using the provided test files.

## 🧪 Test Files Overview

### 1. `test_server.py` - Mock API Server
- **Purpose**: Simulates all backend API endpoints
- **Language**: Python 3.x
- **Port**: 8088 (configurable)
- **Features**: 
  - Complete API mocking
  - CORS enabled for browser testing
  - Realistic response delays
  - Mock data for organizations, articles, agents
  - Error simulation capabilities

### 2. `test_ui.html` - Interactive UI Test Interface  
- **Purpose**: Visual interface for testing the 5-agent pipeline
- **Technology**: Vanilla HTML/CSS/JavaScript
- **Features**:
  - Interactive agent cards
  - Real-time status updates
  - Simulated pipeline execution
  - Purple gradient theme matching the platform
  - Responsive design for all devices

## 🚀 Quick Start

### Option 1: Full System Test (Recommended)

1. **Start the mock API server:**
   ```bash
   python test_server.py
   ```
   
2. **Open the UI test interface:**
   - Open `test_ui.html` in your web browser
   - Or visit: `file:///path/to/blog-poster/test_ui.html`

3. **Test the complete workflow:**
   - Click agent cards to view details
   - Use control buttons to trigger actions
   - Watch real-time status updates
   - Monitor metrics changes

### Option 2: API Testing Only

Test individual endpoints using curl or your preferred API client:

```bash
# Health check
curl http://localhost:8088/health

# Dashboard overview
curl http://localhost:8088/api/dashboard/overview

# Generate article
curl -X POST http://localhost:8088/api/pipeline/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Service Dog Rights"}'

# Fact check content
curl -X POST http://localhost:8088/api/agents/fact-check \
  -H "Content-Type: application/json" \
  -d '{"content": "Service dogs have public access rights."}'
```

## 📡 Available API Endpoints

### GET Endpoints

| Endpoint | Description | Response |
|----------|-------------|----------|
| `/health` | System health check | Service status |
| `/api/dashboard/overview` | Dashboard metrics | Articles, costs, activity |
| `/api/articles` | List all articles | Paginated article list |
| `/api/articles/{id}` | Get specific article | Full article details |
| `/api/agents/status` | Agent pipeline status | Agent health & timing |
| `/api/competitors/analysis` | Competitor insights | Trends & gaps |
| `/api/organization` | Organization details | Plan, usage, billing |
| `/api/team/members` | Team member list | Users & roles |
| `/api/billing/overview` | Billing information | Plan, usage, payments |
| `/api/wordpress/sites` | WordPress sites | Connected sites |

### POST Endpoints

| Endpoint | Description | Payload |
|----------|-------------|---------|
| `/api/pipeline/generate` | Generate new article | `{"topic": "string"}` |
| `/api/agents/fact-check` | Legal fact checking | `{"content": "string"}` |
| `/api/agents/competitor-analysis` | Competitor analysis | `{"industry": "string"}` |
| `/api/wordpress/publish` | Publish to WordPress | `{"article_id": "string"}` |
| `/api/seo/lint` | SEO content validation | `{"content": "string"}` |

## 🎯 Test Scenarios

### 1. Full Article Generation Pipeline

**Test Flow:**
1. Start article generation → `/api/pipeline/generate`
2. Monitor agent execution → `/api/agents/status`
3. Fact check the content → `/api/agents/fact-check`
4. SEO validation → `/api/seo/lint`
5. Publish to WordPress → `/api/wordpress/publish`

**Expected Results:**
- ✅ Article generated in ~3 minutes
- ✅ SEO score > 85
- ✅ Legal accuracy > 95%
- ✅ WordPress publishing successful

### 2. Competitor Monitoring

**Test Flow:**
1. Run competitor analysis → `/api/agents/competitor-analysis`
2. Review trending topics
3. Identify content gaps
4. Generate article on trending topic

**Expected Results:**
- ✅ 8+ competitors scanned
- ✅ 3+ trending topics identified
- ✅ Content gaps highlighted
- ✅ Actionable recommendations

### 3. Multi-Tenant Simulation

**Test Flow:**
1. Switch organization context
2. Verify isolated data
3. Check billing/usage limits
4. Test team member access

**Expected Results:**
- ✅ Data isolation confirmed
- ✅ Separate billing tracking
- ✅ Role-based permissions
- ✅ Organization-specific settings

### 4. Error Handling

**Test Flow:**
1. Send invalid payloads
2. Test with missing API keys
3. Simulate WordPress connection failure
4. Test rate limiting

**Expected Results:**
- ✅ Graceful error responses
- ✅ Helpful error messages
- ✅ Proper HTTP status codes
- ✅ Fallback mechanisms

## 📊 Performance Testing

### Response Time Expectations

| Endpoint | Expected Response Time |
|----------|----------------------|
| `/health` | < 100ms |
| `/api/dashboard/overview` | < 500ms |
| `/api/pipeline/generate` | 2-4 seconds (simulated) |
| `/api/agents/fact-check` | < 1 second |
| `/api/seo/lint` | < 500ms |

### Load Testing

Use Apache Bench (ab) or similar tools:

```bash
# Test concurrent requests
ab -n 100 -c 10 http://localhost:8088/health

# Test article generation under load  
ab -n 20 -c 5 -p article_payload.json -T application/json \
   http://localhost:8088/api/pipeline/generate
```

## 🔧 Configuration Options

### Test Server Configuration

```bash
# Run on different port
python test_server.py 9000

# Environment variables
export TEST_DELAY=0.5  # Response delay in seconds
export MOCK_ERRORS=true  # Enable error simulation
```

### Mock Data Customization

Edit the mock data constants in `test_server.py`:

```python
MOCK_ORGANIZATIONS = [...]  # Add your test organizations
MOCK_ARTICLES = [...]       # Customize article data
MOCK_COMPETITORS = [...]    # Modify competitor list
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Kill process on port 8088
lsof -ti:8088 | xargs kill -9

# Or use different port
python test_server.py 8089
```

**CORS Issues:**
- Ensure browser allows local file access
- Use `--allow-file-access-from-files` Chrome flag
- Or serve test_ui.html via HTTP server

**API Not Responding:**
- Verify Python 3.x is installed
- Check firewall settings
- Confirm server started successfully

### Debug Mode

Enable verbose logging:

```python
# In test_server.py, modify log_message method
def log_message(self, format, *args):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[DEBUG {timestamp}] {format % args}")
```

## 📈 Monitoring & Analytics

### Test Metrics to Track

1. **API Response Times**
   - Average response time per endpoint
   - 95th percentile response times
   - Error rate percentage

2. **Pipeline Performance** 
   - End-to-end generation time
   - Agent execution times
   - Success/failure rates

3. **User Experience**
   - UI responsiveness
   - Error message clarity
   - Workflow completion rates

### Logging

Server logs include:
- Request timestamps
- Endpoint access
- Response status codes
- Processing times

## 🎓 Advanced Testing

### Integration Testing

1. **Docker Container Testing:**
   ```bash
   # Build and test in Docker environment
   docker compose up -d
   python test_server.py
   ```

2. **Database Integration:**
   - Test with actual Supabase instance
   - Verify data persistence
   - Check multi-tenant isolation

3. **External API Testing:**
   - Mock Anthropic Claude API
   - Simulate Jina AI responses
   - Test WordPress WPGraphQL

### Security Testing

1. **Authentication:**
   - Test JWT token validation
   - Verify API key security
   - Check role-based access

2. **Input Validation:**
   - SQL injection attempts
   - XSS payload testing
   - Malformed request handling

## 📝 Test Reporting

### Generate Test Reports

Create comprehensive test reports:

```python
# Example test report generator
def generate_test_report():
    report = {
        "timestamp": datetime.now().isoformat(),
        "endpoints_tested": 15,
        "success_rate": 98.2,
        "avg_response_time": "245ms",
        "issues_found": []
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
```

## 🚀 Next Steps

After successful testing:

1. **Deploy to Production:**
   - Use test results to validate production readiness
   - Monitor real-world performance against test benchmarks

2. **Continuous Testing:**
   - Integrate tests into CI/CD pipeline
   - Set up automated testing schedules
   - Monitor production metrics

3. **User Acceptance Testing:**
   - Share test interface with stakeholders
   - Gather feedback on user experience
   - Validate business requirements

---

## 📞 Support

For testing issues or questions:
- **Documentation**: Check project README.md
- **Issues**: Create GitHub issue with test logs
- **Community**: Join project discussions

**Happy Testing! 🧪✅**