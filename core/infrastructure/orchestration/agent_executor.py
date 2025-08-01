"""Agent executor for task execution."""

import logging
import json
import time
import re
from typing import Dict, Any, List, Optional
from uuid import UUID

from ...domain.entities.agent import Agent, AgentRole
from ...domain.repositories.agent_repository import AgentRepository
from ...application.interfaces.llm_provider_interface import LLMProviderInterface
from ...domain.value_objects.provider_config import ProviderConfig
from ..logging.agent_logger import agent_logger, LogLevel, InteractionType

logger = logging.getLogger(__name__)


class AgentExecutor:
    """
    Executor for AI agents.
    
    This class handles the execution of AI agents with appropriate tools
    and LLM backends.
    """
    
    def __init__(
        self, 
        agent_repository: AgentRepository,
        llm_provider: LLMProviderInterface,
        provider_config: ProviderConfig
    ):
        self.agent_repository = agent_repository
        self.llm_provider = llm_provider
        self.provider_config = provider_config
        self.tools_registry = {}
    
    def register_tool(self, tool_name: str, tool_function: callable, description: str):
        """Register a tool for agent use."""
        self.tools_registry[tool_name] = {
            'function': tool_function,
            'description': description
        }
    
    def register_tools(self, tools: Dict[str, Dict[str, Any]]):
        """Register multiple tools at once."""
        for tool_name, tool_info in tools.items():
            self.register_tool(
                tool_name, 
                tool_info['function'], 
                tool_info.get('description', f"Tool: {tool_name}")
            )
    
    async def execute_agent(
        self,
        agent: Agent,
        task_description: str,
        context: Dict[str, Any] = None
    ) -> str:
        """
        Execute an agent with a specific task.

        Args:
            agent: The agent to execute
            task_description: Description of the task to perform
            context: Additional context for the agent

        Returns:
            Agent's output as a string
        """
        context = context or {}

        # Start agent session with detailed logging
        session_id = agent_logger.start_agent_session(
            agent_id=str(agent.id),
            agent_name=agent.name,
            task_id=context.get('task_id', 'unknown'),
            workflow_id=context.get('workflow_id', 'unknown'),
            task_description=task_description
        )

        try:
            # Log agent thinking process
            agent_logger.log_agent_thinking(
                session_id=session_id,
                thought=f"Starting task execution for: {task_description[:100]}...",
                reasoning=f"Agent role: {agent.role.value}, Available tools: {len(agent.tools)}",
                next_action="Preparing system message and prompt"
            )

            # Prepare system message
            system_message = self._prepare_system_message(agent, context)

            # Prepare tools for this agent
            agent_tools = self._get_agent_tools(agent)

            # Log available tools
            if agent_tools:
                agent_logger.log_agent_thinking(
                    session_id=session_id,
                    thought=f"Tools available: {', '.join(agent_tools)}",
                    reasoning="These tools can be used to enhance the response",
                    next_action="Preparing prompt with tool instructions"
                )

            # Prepare prompt
            prompt = self._prepare_prompt(task_description, context, agent_tools)

            # Log LLM request
            request_id = agent_logger.log_llm_request(
                session_id=session_id,
                provider=self.provider_config.provider.value,
                model=self.provider_config.model,
                prompt=prompt,
                system_message=system_message
            )

            # Execute LLM call with timing
            start_time = time.time()
            response = await self.llm_provider.generate_content(
                prompt=prompt,
                config=self.provider_config,
                system_message=system_message
            )
            duration_ms = (time.time() - start_time) * 1000

            # Estimate tokens and cost (simplified)
            estimated_tokens = len(prompt.split()) + len(response.split())
            estimated_cost = self._estimate_cost(estimated_tokens, self.provider_config.provider.value)

            # Log LLM response
            agent_logger.log_llm_response(
                session_id=session_id,
                request_id=request_id,
                provider=self.provider_config.provider.value,
                model=self.provider_config.model,
                response=response,
                tokens_used=estimated_tokens,
                cost_usd=estimated_cost,
                duration_ms=duration_ms
            )

            # Process tool calls if any
            final_response = await self.process_tool_calls(response, session_id)

            # End agent session successfully
            agent_logger.end_agent_session(
                session_id=session_id,
                success=True,
                final_output=final_response
            )

            return final_response

        except Exception as e:
            # End agent session with error
            agent_logger.end_agent_session(
                session_id=session_id,
                success=False,
                error_message=str(e)
            )
            raise
    
    def _prepare_system_message(self, agent: Agent, context: Dict[str, Any] = None) -> str:
        """Prepare system message for the agent."""
        context = context or {}
        
        # Start with agent's system message
        if agent.system_message:
            system_message = agent.system_message
        else:
            # Default system messages based on role
            role_messages = {
                AgentRole.RESEARCHER: "You are an expert researcher who finds accurate, relevant information and presents it clearly.",
                AgentRole.WRITER: "You are an expert writer who creates engaging, well-structured content tailored to specific audiences.",
                AgentRole.EDITOR: "You are an expert editor who refines content for clarity, coherence, and alignment with style guidelines.",
                AgentRole.ANALYST: "You are an expert analyst who examines data and information to extract meaningful insights.",
                AgentRole.PLANNER: "You are an expert planner who organizes complex tasks into clear, actionable steps."
            }
            system_message = role_messages.get(agent.role, "You are an AI assistant helping with content generation.")
        
        # Add agent backstory if available
        if agent.backstory:
            system_message += f"\n\n{agent.backstory}"
        
        # Add agent goal if available
        if agent.goal:
            system_message += f"\n\nYour goal is: {agent.goal}"
        
        # Add context-specific information
        if context.get('client_profile'):
            system_message += f"\n\nYou are working for client: {context.get('client_profile')}"
        
        if context.get('target_audience'):
            system_message += f"\n\nThe target audience is: {context.get('target_audience')}"
        
        # Add tools information
        tools_info = self._get_agent_tools_descriptions(agent)
        if tools_info:
            system_message += f"\n\nYou have access to the following tools:\n{tools_info}"
            system_message += "\n\nIMPORTANT: When you need to use a tool, format your response EXACTLY like this:"
            system_message += "\n[rag_get_client_content] client_name [/rag_get_client_content]"
            system_message += "\n[web_search] your search query [/web_search]"
            system_message += "\n[rag_search_content] client_name, search_query [/rag_search_content]"
            system_message += "\n\nReplace TOOL_NAME with the exact tool name from the list above. Do NOT use generic placeholders like 'TOOL_NAME'."
        
        return system_message
    
    def _prepare_prompt(
        self, 
        task_description: str, 
        context: Dict[str, Any] = None,
        tools: List[str] = None
    ) -> str:
        """Prepare the prompt for the agent."""
        context = context or {}
        prompt_parts = [task_description]
        
        # Add context information
        if context:
            context_str = "\n\n## Context Information\n"
            for key, value in context.items():
                if key not in ['client_profile', 'target_audience'] and value:
                    context_str += f"\n- {key}: {value}"
            prompt_parts.append(context_str)
        
        # Add tools reminder if tools are available
        if tools:
            tools_reminder = "\n\n## Available Tools\n"
            tools_reminder += "You can use these tools to enhance your response:\n"
            for tool in tools:
                if tool == "rag_get_client_content":
                    tools_reminder += f"- {tool}: Use [rag_get_client_content] client_name [/rag_get_client_content] to retrieve all content for a client\n"
                elif tool == "rag_search_content":
                    tools_reminder += f"- {tool}: Use [rag_search_content] client_name, search_query [/rag_search_content] to search within client content\n"
                elif tool == "web_search":
                    tools_reminder += f"- {tool}: Use [web_search] your search query [/web_search] to search the web for current information\n"
                elif tool == "web_search_financial":
                    tools_reminder += f"- {tool}: Use [web_search_financial] topic, exclude_topics [/web_search_financial] for financial content\n"
                else:
                    tools_reminder += f"- {tool}: Use [{tool}] your input [/{tool}]\n"

            tools_reminder += "\n⚠️ CRITICAL: Use the EXACT tool names shown above. Do NOT use placeholders like 'TOOL_NAME'."
            prompt_parts.append(tools_reminder)
        
        # Add final instructions
        prompt_parts.append("\n\nPlease provide a comprehensive response to the task.")
        
        return "\n".join(prompt_parts)
    
    def _get_agent_tools(self, agent: Agent) -> List[str]:
        """Get the list of tools available to this agent."""
        available_tools = []
        
        for tool_name in agent.tools:
            if tool_name in self.tools_registry:
                available_tools.append(tool_name)
        
        return available_tools
    
    def _get_agent_tools_descriptions(self, agent: Agent) -> str:
        """Get descriptions of tools available to this agent."""
        tool_descriptions = []
        
        for tool_name in agent.tools:
            if tool_name in self.tools_registry:
                description = self.tools_registry[tool_name]['description']
                tool_descriptions.append(f"- {tool_name}: {description}")
        
        return "\n".join(tool_descriptions)
    
    async def process_tool_calls(self, agent_response: str, session_id: str = None) -> str:
        """
        Process tool calls in the agent's response.

        This function looks for tool calls in the format [TOOL_NAME] input [/TOOL_NAME]
        and executes the corresponding tools.

        Args:
            agent_response: The agent's response text
            session_id: Agent session ID for logging

        Returns:
            Updated response with tool results
        """
        # Find all tool calls
        tool_pattern = r'\[(\w+)\](.*?)\[/\1\]'
        tool_calls = re.findall(tool_pattern, agent_response, re.DOTALL)

        if not tool_calls:
            if session_id:
                agent_logger.log_agent_thinking(
                    session_id=session_id,
                    thought="No tool calls detected in response",
                    reasoning="Agent provided direct response without using tools",
                    next_action="Returning response as-is"
                )
            return agent_response

        if session_id:
            agent_logger.log_agent_thinking(
                session_id=session_id,
                thought=f"Detected {len(tool_calls)} tool calls",
                reasoning=f"Tools to execute: {[call[0] for call in tool_calls]}",
                next_action="Processing tool calls sequentially"
            )

        # Process each tool call
        for tool_name, tool_input in tool_calls:
            if tool_name in self.tools_registry:
                # Log tool call start
                call_id = None
                if session_id:
                    call_id = agent_logger.log_tool_call(
                        session_id=session_id,
                        tool_name=tool_name,
                        tool_input=tool_input.strip(),
                        tool_description=self.tools_registry[tool_name]['description']
                    )

                try:
                    # Execute the tool with timing
                    start_time = time.time()
                    tool_function = self.tools_registry[tool_name]['function']
                    tool_result = await tool_function(tool_input.strip())
                    duration_ms = (time.time() - start_time) * 1000

                    # Log successful tool response
                    if session_id and call_id:
                        agent_logger.log_tool_response(
                            session_id=session_id,
                            call_id=call_id,
                            tool_name=tool_name,
                            tool_output=tool_result,
                            duration_ms=duration_ms,
                            success=True
                        )

                    # Replace the tool call with the result
                    tool_call = f"[{tool_name}]{tool_input}[/{tool_name}]"
                    tool_result_text = f"[{tool_name} RESULT]\n{tool_result}\n[/{tool_name} RESULT]"
                    agent_response = agent_response.replace(tool_call, tool_result_text)

                except Exception as e:
                    duration_ms = (time.time() - start_time) * 1000 if 'start_time' in locals() else 0

                    # Log tool error
                    if session_id and call_id:
                        agent_logger.log_tool_error(
                            session_id=session_id,
                            call_id=call_id,
                            tool_name=tool_name,
                            error=e,
                            duration_ms=duration_ms
                        )

                    # Replace with error message
                    tool_call = f"[{tool_name}]{tool_input}[/{tool_name}]"
                    error_text = f"[{tool_name} ERROR] {str(e)} [/{tool_name} ERROR]"
                    agent_response = agent_response.replace(tool_call, error_text)
            else:
                # Tool not found - log error
                if session_id:
                    call_id = agent_logger.log_tool_call(
                        session_id=session_id,
                        tool_name=tool_name,
                        tool_input=tool_input.strip(),
                        tool_description="Tool not found"
                    )

                    agent_logger.log_tool_error(
                        session_id=session_id,
                        call_id=call_id,
                        tool_name=tool_name,
                        error=Exception(f"Tool '{tool_name}' not found in registry"),
                        duration_ms=0
                    )

                tool_call = f"[{tool_name}]{tool_input}[/{tool_name}]"
                error_text = f"[{tool_name} ERROR] Tool not found [/{tool_name} ERROR]"
                agent_response = agent_response.replace(tool_call, error_text)

        return agent_response

    def _estimate_cost(self, tokens: int, provider: str) -> float:
        """Estimate cost based on tokens and provider."""
        # Simplified cost estimation (per 1K tokens)
        cost_per_1k = {
            'openai': 0.002,  # GPT-4 approximate
            'anthropic': 0.008,  # Claude approximate
            'deepseek': 0.0002  # DeepSeek approximate
        }

        rate = cost_per_1k.get(provider.lower(), 0.002)
        return (tokens / 1000) * rate
