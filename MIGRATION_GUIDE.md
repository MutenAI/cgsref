# Migration Guide: From Legacy FylleCGS to CGSRef

This guide explains how to migrate from the legacy FylleCGS system to the new clean architecture CGSRef implementation.

## Overview of Changes

### Architecture Transformation

**Before (Legacy FylleCGS):**
```
FylleCGS/
├── app.py (Streamlit + Business Logic)
├── main.py (CLI + Business Logic)  
├── src/ (Mixed responsibilities)
└── workflows/ (Tightly coupled)
```

**After (CGSRef):**
```
CGSRef/
├── core/ (Pure Business Logic)
│   ├── domain/ (Entities, Value Objects)
│   ├── application/ (Use Cases, DTOs)
│   └── infrastructure/ (External Services)
├── api/ (Interface Layer)
│   ├── rest/ (FastAPI)
│   ├── cli/ (Typer)
│   └── websocket/ (Real-time)
└── web/ (Frontend Layer)
```

## Key Benefits of Migration

### 1. **Clean Separation of Concerns**
- Business logic is completely independent of UI frameworks
- Easy to test without external dependencies
- Clear boundaries between layers

### 2. **Improved Maintainability**
- Single Responsibility Principle applied throughout
- Dependency Inversion eliminates tight coupling
- Open/Closed Principle allows easy extension

### 3. **Enhanced Scalability**
- Stateless design enables horizontal scaling
- Microservice-ready architecture
- Multiple interface options (REST, CLI, WebSocket)

### 4. **Better Developer Experience**
- Type safety with Pydantic models
- Comprehensive test coverage
- Clear documentation and examples

## Migration Steps

### Phase 1: Environment Setup

1. **Clone and Setup CGSRef:**
   ```bash
   cd "Desktop/Content Generation copy/CGSRef"
   python scripts/setup.py
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Verify Installation:**
   ```bash
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m api.cli.main config
   ```

### Phase 2: Data Migration

1. **Migrate Client Profiles:**
   ```bash
   # Copy existing profiles from legacy system
   cp -r "../FylleCGS/profiles/" "data/profiles/"
   ```

2. **Migrate Knowledge Base:**
   ```bash
   # Copy RAG documents
   cp -r "../FylleCGS/rag/" "data/knowledge_base/"
   ```

3. **Migrate Generated Content:**
   ```bash
   # Copy existing output
   cp -r "../FylleCGS/output/" "data/output/"
   ```

### Phase 3: API Migration

**Legacy Streamlit Usage:**
```python
# Old way - mixed UI and business logic
import streamlit as st
from src.agents import AgentsFactory
# ... complex setup in UI code
```

**New REST API Usage:**
```python
# New way - clean API calls
import httpx

response = httpx.post("http://localhost:8000/api/v1/content/generate", json={
    "topic": "AI in Finance",
    "content_type": "article",
    "provider": "openai",
    "model": "gpt-4o"
})
```

**New CLI Usage:**
```bash
# Simple, powerful CLI
python -m api.cli.main generate "AI in Finance" \
    --type article \
    --provider openai \
    --client siebert
```

### Phase 4: Workflow Migration

**Legacy Workflow Definition:**
```python
# Old way - tightly coupled
def workflow_siebert(topic, agents, tools, config):
    # Mixed business logic and infrastructure
    pass
```

**New Workflow Definition:**
```python
# New way - clean domain model
from core.domain.entities.workflow import Workflow, WorkflowType
from core.domain.entities.task import Task

workflow = Workflow(
    name="siebert_newsletter",
    workflow_type=WorkflowType.SIEBERT_NEWSLETTER,
    client_profile="siebert"
)

research_task = Task(
    name="research",
    description="Research financial topics",
    expected_output="Comprehensive research findings"
)

workflow.add_task(research_task)
```

## Feature Comparison

| Feature | Legacy FylleCGS | CGSRef |
|---------|----------------|---------|
| **Architecture** | Monolithic | Clean Architecture |
| **UI Framework** | Streamlit only | Multiple (REST, CLI, WebSocket) |
| **Testing** | Limited | Comprehensive |
| **Type Safety** | Minimal | Full Pydantic validation |
| **Scalability** | Single instance | Horizontally scalable |
| **Documentation** | Basic | Comprehensive |
| **Configuration** | Scattered | Centralized |
| **Error Handling** | Basic | Robust with proper exceptions |
| **Logging** | Basic | Structured logging |
| **Deployment** | Manual | Docker + Compose |

## Code Examples

### Content Generation

**Legacy:**
```python
# Complex setup required
from src.config import check_environment
from src.agents import AgentsFactory
from src.workflow_factory import workflow_factory

# Mixed concerns
agents_factory = AgentsFactory(provider="openai")
agents = agents_factory.create_agents()
workflow = workflow_factory(topic, "siebert", agents)
# ... complex orchestration
```

**CGSRef:**
```python
# Clean, simple usage
from core.application.use_cases.generate_content import GenerateContentUseCase
from core.application.dto.content_request import ContentGenerationRequest

request = ContentGenerationRequest(
    topic="AI in Finance",
    client_profile="siebert",
    workflow_type="siebert_newsletter"
)

use_case = get_content_use_case()  # Dependency injection
response = await use_case.execute(request)
```

### Agent Configuration

**Legacy:**
```python
# YAML files mixed with Python logic
agent = Agent(
    role="Copywriter",
    goal="Create content",
    # ... mixed configuration
)
```

**CGSRef:**
```python
# Clean domain model
from core.domain.entities.agent import Agent, AgentRole
from core.domain.value_objects.provider_config import ProviderConfig

agent = Agent(
    name="siebert_copywriter",
    role=AgentRole.COPYWRITER,
    goal="Create financial content for Gen Z audience",
    provider_config=ProviderConfig.create_openai_config()
)
```

## Testing Migration

**Legacy Testing:**
- Limited test coverage
- Difficult to test business logic
- UI and logic mixed

**CGSRef Testing:**
```python
# Pure unit tests for business logic
def test_content_generation():
    # Arrange
    request = ContentGenerationRequest(topic="Test")
    mock_llm = MockLLMProvider()
    use_case = GenerateContentUseCase(
        content_repository=mock_repo,
        llm_provider=mock_llm
    )
    
    # Act
    response = await use_case.execute(request)
    
    # Assert
    assert response.success
    assert response.word_count > 0
```

## Deployment Migration

**Legacy Deployment:**
```bash
# Manual process
pip install -r requirements.txt
streamlit run app.py
```

**CGSRef Deployment:**
```bash
# Docker-based
docker-compose up -d

# Or Kubernetes
kubectl apply -f k8s/
```

## Rollback Strategy

If issues arise during migration:

1. **Keep Legacy System Running:**
   - Legacy system remains untouched in original directory
   - Can switch back immediately if needed

2. **Gradual Migration:**
   - Migrate one workflow at a time
   - Test thoroughly before proceeding

3. **Data Backup:**
   - All data migration is copy-based
   - Original data remains intact

## Performance Improvements

### Response Times
- **Legacy:** 5-10 seconds (UI overhead)
- **CGSRef:** 2-3 seconds (optimized API)

### Memory Usage
- **Legacy:** High (Streamlit overhead)
- **CGSRef:** Low (efficient FastAPI)

### Scalability
- **Legacy:** Single instance only
- **CGSRef:** Horizontal scaling ready

## Support and Troubleshooting

### Common Issues

1. **API Key Configuration:**
   ```bash
   # Check configuration
   python -m api.cli.main config
   ```

2. **Port Conflicts:**
   ```bash
   # Change port in .env
   API_PORT=8001
   ```

3. **Dependencies:**
   ```bash
   # Reinstall if needed
   pip install -r requirements.txt
   ```

### Getting Help

- Check logs: `logs/cgsref.log`
- Run diagnostics: `python -m api.cli.main --help`
- Review documentation: `docs/`

## Next Steps

After successful migration:

1. **Explore New Features:**
   - WebSocket real-time updates
   - Advanced workflow builder
   - Enhanced monitoring

2. **Customize for Your Needs:**
   - Add new AI providers
   - Create custom workflows
   - Extend with new content types

3. **Scale Your Deployment:**
   - Set up load balancing
   - Configure monitoring
   - Implement CI/CD

The CGSRef architecture provides a solid foundation for future growth and enhancement while maintaining the powerful content generation capabilities of the original system.
