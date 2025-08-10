---
allowed-tools: Read, Write, Bash(python:*), Task
description: Generate comprehensive Product Requirements Prompt using research and LocalDocs
---

# Enhanced PRP Generation

Generate comprehensive Product Requirements Prompts leveraging both Jina research and LocalDocs collections for accurate, context-rich implementation guidance.

## PRP Generation Process

### Phase 1: Context Collection
1. **Assess available research**:
   - Check `research/` directories for relevant technology summaries
   - Review `docs/` collections for API references and deployment guides
   - Identify gaps in current documentation

2. **Gather requirements from user input**:
   - Parse feature request from $ARGUMENTS
   - Identify technologies, integrations, and deployment requirements
   - Determine complexity level and implementation approach

### Phase 2: Research Integration
1. **Leverage Jina research** (comprehensive context):
   ```bash
   # Read technology summaries for deep context
   cat research/*/llm.txt
   ```

2. **Reference LocalDocs collections** (specific APIs):
   ```markdown
   # Use @file references for precise API documentation
   See @docs/api-integration/auth-methods.md for authentication implementation.
   See @docs/deployment-workflow/portainer-api.md for container deployment.
   ```

### Phase 3: PRP Document Construction
1. **Use enhanced PRP template** with:
   - Research-backed technology choices
   - Specific API endpoints and authentication methods
   - Deployment pipeline requirements
   - Testing and validation approaches

2. **Include documentation references**:
   - Direct links to research summaries
   - @file references to LocalDocs collections
   - Cross-references between related components

### Phase 4: Technical Specification
1. **Architecture decisions** based on research findings
2. **Implementation patterns** from established documentation
3. **Error handling approaches** from API documentation
4. **Deployment requirements** from infrastructure guides

## Enhanced PRP Template Structure

### 1. Executive Summary
- **Feature Description**: Clear, concise feature overview
- **Business Value**: Why this feature matters
- **Technical Approach**: High-level implementation strategy
- **Research Foundation**: Key documentation sources used

### 2. Technical Requirements

#### Core Functionality
```markdown
**Primary Features**:
- [Feature 1] - Based on research/[tech]/llm.txt analysis
- [Feature 2] - See @docs/api-integration/[hash].md for implementation details
- [Feature 3] - Following patterns from @docs/deployment-workflow/[hash].md

**API Integration**:
- Authentication: See @docs/auth-methods/[hash].md
- Data Models: Referenced in research/[tech]/page2/schemas.md
- Rate Limiting: See @docs/api-limits/[hash].md
```

#### Non-Functional Requirements
- **Performance**: Response times, throughput requirements
- **Security**: Authentication, authorization, data protection
- **Scalability**: Growth patterns, load expectations
- **Reliability**: Uptime targets, error handling, recovery

### 3. Architecture & Design

#### System Architecture
```markdown
**Component Overview**:
- Frontend: [Technology] - See research/[tech]/llm.txt for capabilities
- Backend: [API Framework] - See @docs/api-framework/[hash].md
- Database: [DB Technology] - See @docs/database-setup/[hash].md
- Infrastructure: See @docs/deployment-workflow/claude-refs.md

**Integration Points**:
- External APIs: See @docs/external-apis/[hash].md
- Authentication Systems: See @docs/auth-integration/[hash].md
- Monitoring & Logging: See @docs/monitoring-setup/[hash].md
```

#### Data Models
- **Database Schema**: Based on research findings
- **API Contracts**: Following documented patterns
- **State Management**: Client-side data handling

### 4. Implementation Approach

#### Development Phases
1. **Phase 1**: Core functionality (MVP)
2. **Phase 2**: Integration and testing  
3. **Phase 3**: Performance optimization and deployment
4. **Phase 4**: Monitoring and maintenance

#### Technical Decisions
```markdown
**Framework Choices**:
- [Framework]: Selected based on research/[tech]/page1/comparison.md
- [Database]: Chosen per @docs/database-options/[hash].md analysis
- [Deployment]: Following @docs/deployment-workflow/claude-refs.md

**Implementation Patterns**:
- Error Handling: See @docs/error-patterns/[hash].md
- Authentication: See @docs/auth-implementation/[hash].md  
- Testing Strategy: See @docs/testing-approaches/[hash].md
```

### 5. Acceptance Criteria

#### Functional Testing
- [ ] **Feature 1 Tests**: [Specific test scenarios]
- [ ] **API Integration Tests**: Verify all endpoints work as documented
- [ ] **Authentication Tests**: Validate security implementation
- [ ] **Error Handling Tests**: Ensure graceful failure modes

#### Non-Functional Testing  
- [ ] **Performance Tests**: Meet documented requirements
- [ ] **Security Tests**: Pass security audit checklist
- [ ] **Deployment Tests**: Successful deployment via documented process

#### Documentation Requirements
- [ ] **API Documentation**: Complete endpoint documentation
- [ ] **Deployment Guide**: Step-by-step deployment instructions
- [ ] **User Documentation**: End-user feature documentation

### 6. Research References

#### Primary Research Sources
```markdown
**Comprehensive Analysis**:
- research/[tech]/llm.txt - Technology overview and capabilities
- research/[integration]/llm.txt - Integration patterns and approaches

**API Documentation**:
- @docs/api-reference/claude-refs.md - Current API collection
- @docs/auth-methods/claude-refs.md - Authentication approaches
- @docs/deployment-workflow/claude-refs.md - Infrastructure setup

**Best Practices**:
- memory/[tech]-best-practices.md - Lessons learned
- memory/deployment-patterns.md - Proven deployment approaches
```

#### Validation Sources
- **Official Documentation**: Links to authoritative sources
- **Community Resources**: Validated community patterns
- **Security Guidelines**: Industry standard security practices

## PRP Generation Commands

### Generate Standard PRP
```bash
/generate-prp "Add user authentication with OAuth2 and JWT tokens"
```

### Generate with Specific Technology Focus
```bash
/generate-prp "Create FastAPI backend with Supabase integration and Portainer deployment"
```

### Generate with Research Integration
```bash
/generate-prp "Build React dashboard with real-time updates using research/websockets/llm.txt findings"
```

## Quality Assurance

### PRP Review Checklist
- [ ] **Research Integration**: All claims backed by research or documentation
- [ ] **Technical Feasibility**: Implementation approach is validated
- [ ] **Deployment Strategy**: Clear path from development to production
- [ ] **Testing Approach**: Comprehensive testing strategy defined
- [ ] **Documentation References**: All @file references are valid and accessible

### Implementation Validation
- [ ] **API Compatibility**: Endpoints match documented specifications  
- [ ] **Authentication Flow**: Security implementation follows best practices
- [ ] **Error Handling**: Robust error handling per documentation guidelines
- [ ] **Performance Targets**: Meets requirements based on research findings

This enhanced PRP generation process ensures implementation guidance is grounded in comprehensive research while leveraging organized documentation collections for precise technical specifications.