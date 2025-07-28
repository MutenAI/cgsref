"""FastAPI dependencies for dependency injection."""

from functools import lru_cache
from typing import Optional

from core.application.use_cases.generate_content import GenerateContentUseCase
from core.infrastructure.repositories.file_content_repository import FileContentRepository
from core.infrastructure.repositories.yaml_agent_repository import YamlAgentRepository
from core.infrastructure.repositories.file_workflow_repository import FileWorkflowRepository
from core.infrastructure.external_services.openai_adapter import OpenAIAdapter
from core.infrastructure.config.settings import get_settings


@lru_cache()
def get_content_repository() -> FileContentRepository:
    """Get content repository instance."""
    settings = get_settings()
    return FileContentRepository(settings.output_dir)


@lru_cache()
def get_agent_repository() -> YamlAgentRepository:
    """Get agent repository instance."""
    settings = get_settings()
    return YamlAgentRepository(settings.profiles_dir)


@lru_cache()
def get_workflow_repository() -> FileWorkflowRepository:
    """Get workflow repository instance."""
    settings = get_settings()
    return FileWorkflowRepository(settings.workflows_dir)


@lru_cache()
def get_llm_provider() -> OpenAIAdapter:
    """Get LLM provider instance."""
    settings = get_settings()
    return OpenAIAdapter(settings.openai_api_key)


def get_content_use_case() -> GenerateContentUseCase:
    """Get content generation use case."""
    settings = get_settings()

    # Create provider config
    from core.domain.value_objects.provider_config import ProviderConfig, LLMProvider
    provider_config = ProviderConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-4o",
        api_key=settings.openai_api_key
    )

    return GenerateContentUseCase(
        content_repository=get_content_repository(),
        workflow_repository=get_workflow_repository(),
        agent_repository=get_agent_repository(),
        llm_provider=get_llm_provider(),
        provider_config=provider_config,
        rag_service=None,  # Would be implemented later
        serper_api_key=settings.serper_api_key
    )
