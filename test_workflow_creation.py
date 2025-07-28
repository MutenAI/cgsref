#!/usr/bin/env python3
"""
Test workflow creation to debug the DRAFT status issue.
"""

import sys
import os
import asyncio
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_workflow_creation():
    """Test workflow creation and status."""
    try:
        # Import required modules
        from core.application.use_cases.generate_content import GenerateContentUseCase
        from core.application.dto.content_request import ContentGenerationRequest
        from core.domain.entities.content import ContentType, ContentFormat
        from core.domain.value_objects.provider_config import ProviderConfig, LLMProvider
        from core.infrastructure.config.settings import get_settings
        
        # Create a simple use case instance (mock dependencies)
        class MockRepository:
            async def save(self, entity):
                return entity
            async def get_by_type(self, workflow_type):
                return []
            async def clone_workflow(self, workflow_id, name):
                return None
            async def update(self, entity):
                return entity
        
        class MockOrchestrator:
            async def execute_workflow(self, workflow, context, verbose=True):
                logger.info(f"🔍 Mock orchestrator called with workflow status: {workflow.status}")
                logger.info(f"🔍 Workflow can_start: {workflow.can_start()}")
                logger.info(f"🔍 Workflow tasks: {len(workflow.tasks)}")
                for task in workflow.tasks:
                    logger.info(f"   Task: {task.name} - Status: {task.status}")
                
                # Try to start the workflow
                try:
                    workflow.start()
                    logger.info("✅ Workflow started successfully")
                    return {"final_output": "Mock content generated", "success": True}
                except Exception as e:
                    logger.error(f"❌ Failed to start workflow: {e}")
                    return {"final_output": "", "success": False, "error": str(e)}
        
        class MockAgentExecutor:
            pass
        
        # Create use case
        settings = get_settings()
        use_case = GenerateContentUseCase(
            content_repository=MockRepository(),
            workflow_repository=MockRepository(),
            agent_repository=MockRepository(),
            llm_provider=None,
            provider_config=None,
            serper_api_key=settings.serper_api_key
        )
        
        # Test context
        context = {
            'topic': 'Test AI Article',
            'target_audience': 'developers',
            'tone': 'professional',
            'length': 'medium'
        }
        
        logger.info("🧪 Testing legacy workflow creation...")
        
        # Test _create_legacy_workflow directly
        workflow = await use_case._create_legacy_workflow("enhanced_article", context)
        
        logger.info(f"📊 Created workflow:")
        logger.info(f"   Name: {workflow.name}")
        logger.info(f"   Status: {workflow.status}")
        logger.info(f"   Tasks: {len(workflow.tasks)}")
        logger.info(f"   Can start: {workflow.can_start()}")
        
        for task in workflow.tasks:
            logger.info(f"   Task: {task.name} - Status: {task.status}")
        
        # Test _execute_legacy_workflow
        logger.info("🧪 Testing legacy workflow execution...")
        result = await use_case._execute_legacy_workflow("enhanced_article", context)
        
        logger.info(f"📊 Execution result:")
        logger.info(f"   Success: {result.get('success', 'unknown')}")
        logger.info(f"   Final output: {result.get('final_output', 'none')[:100]}...")
        logger.info(f"   Error: {result.get('error', 'none')}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_workflow_creation())
