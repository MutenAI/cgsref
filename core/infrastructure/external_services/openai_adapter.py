"""OpenAI service adapter."""

import logging
from typing import Dict, List, Optional, Any, AsyncGenerator
import openai
from openai import AsyncOpenAI

from ...application.interfaces.llm_provider_interface import (
    LLMProviderInterface, 
    LLMResponse, 
    LLMStreamChunk
)
from ...domain.value_objects.provider_config import ProviderConfig, LLMProvider

logger = logging.getLogger(__name__)


class OpenAIAdapter(LLMProviderInterface):
    """
    OpenAI service adapter implementing LLMProviderInterface.
    
    This adapter handles all interactions with OpenAI's API,
    providing a clean interface for the application layer.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._client: Optional[AsyncOpenAI] = None
    
    def _get_client(self, config: ProviderConfig) -> AsyncOpenAI:
        """Get or create OpenAI client."""
        if self._client is None or config.api_key != self.api_key:
            api_key = config.api_key or self.api_key
            if not api_key:
                raise ValueError("OpenAI API key is required")
            
            client_kwargs = {"api_key": api_key}
            if config.base_url:
                client_kwargs["base_url"] = config.base_url
            
            self._client = AsyncOpenAI(**client_kwargs)
            self.api_key = api_key
        
        return self._client
    
    async def generate_content(
        self, 
        prompt: str, 
        config: ProviderConfig,
        system_message: Optional[str] = None
    ) -> str:
        """Generate content using OpenAI."""
        response = await self.generate_content_detailed(prompt, config, system_message)
        return response.content
    
    async def generate_content_detailed(
        self, 
        prompt: str, 
        config: ProviderConfig,
        system_message: Optional[str] = None
    ) -> LLMResponse:
        """Generate content with detailed response."""
        if config.provider != LLMProvider.OPENAI:
            raise ValueError(f"Expected OpenAI provider, got {config.provider}")
        
        client = self._get_client(config)
        
        # Build messages
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request parameters
        request_params = {
            "model": config.model,
            "messages": messages,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
        }
        
        if config.max_tokens:
            request_params["max_tokens"] = config.max_tokens
        
        # Add any additional parameters
        request_params.update(config.additional_params)
        
        try:
            logger.debug(f"Making OpenAI request with model: {config.model}")
            response = await client.chat.completions.create(**request_params)
            
            choice = response.choices[0]
            content = choice.message.content or ""
            
            return LLMResponse(
                content=content,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                model=response.model,
                finish_reason=choice.finish_reason or "",
                metadata={
                    "response_id": response.id,
                    "created": response.created
                }
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def generate_content_stream(
        self, 
        prompt: str, 
        config: ProviderConfig,
        system_message: Optional[str] = None
    ) -> AsyncGenerator[LLMStreamChunk, None]:
        """Generate content with streaming response."""
        if config.provider != LLMProvider.OPENAI:
            raise ValueError(f"Expected OpenAI provider, got {config.provider}")
        
        client = self._get_client(config)
        
        # Build messages
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request parameters
        request_params = {
            "model": config.model,
            "messages": messages,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "stream": True
        }
        
        if config.max_tokens:
            request_params["max_tokens"] = config.max_tokens
        
        request_params.update(config.additional_params)
        
        try:
            stream = await client.chat.completions.create(**request_params)
            
            async for chunk in stream:
                if chunk.choices:
                    choice = chunk.choices[0]
                    if choice.delta.content:
                        yield LLMStreamChunk(
                            content=choice.delta.content,
                            is_final=choice.finish_reason is not None,
                            metadata={
                                "chunk_id": chunk.id,
                                "finish_reason": choice.finish_reason
                            }
                        )
                    
                    if choice.finish_reason:
                        yield LLMStreamChunk(
                            content="",
                            is_final=True,
                            metadata={"finish_reason": choice.finish_reason}
                        )
                        break
                        
        except Exception as e:
            logger.error(f"OpenAI streaming error: {str(e)}")
            raise
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        config: ProviderConfig
    ) -> LLMResponse:
        """Perform chat completion."""
        if config.provider != LLMProvider.OPENAI:
            raise ValueError(f"Expected OpenAI provider, got {config.provider}")
        
        client = self._get_client(config)
        
        request_params = {
            "model": config.model,
            "messages": messages,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
        }
        
        if config.max_tokens:
            request_params["max_tokens"] = config.max_tokens
        
        request_params.update(config.additional_params)
        
        try:
            response = await client.chat.completions.create(**request_params)
            
            choice = response.choices[0]
            content = choice.message.content or ""
            
            return LLMResponse(
                content=content,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                model=response.model,
                finish_reason=choice.finish_reason or ""
            )
            
        except Exception as e:
            logger.error(f"OpenAI chat completion error: {str(e)}")
            raise
    
    async def validate_config(self, config: ProviderConfig) -> bool:
        """Validate OpenAI configuration."""
        try:
            if config.provider != LLMProvider.OPENAI:
                return False
            
            if not config.api_key and not self.api_key:
                return False
            
            # Test with a simple request
            await self.generate_content("Test", config)
            return True
            
        except Exception:
            return False
    
    async def get_available_models(self, config: ProviderConfig) -> List[str]:
        """Get available OpenAI models."""
        try:
            client = self._get_client(config)
            models = await client.models.list()
            return [model.id for model in models.data if "gpt" in model.id.lower()]
        except Exception:
            # Return default models if API call fails
            return config.get_available_models()
    
    async def estimate_tokens(self, text: str, model: str) -> int:
        """Estimate token count (simplified implementation)."""
        # This is a rough estimation - in production, use tiktoken
        return len(text.split()) * 1.3  # Rough approximation
    
    async def check_health(self, config: ProviderConfig) -> Dict[str, Any]:
        """Check OpenAI service health."""
        try:
            client = self._get_client(config)
            models = await client.models.list()
            
            return {
                "status": "healthy",
                "provider": "openai",
                "models_available": len(models.data),
                "api_key_valid": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "provider": "openai",
                "error": str(e),
                "api_key_valid": False
            }
