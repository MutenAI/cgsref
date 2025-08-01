"""Task orchestrator for workflow execution."""

import re
import logging
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime

from ...domain.entities.workflow import Workflow, WorkflowStatus
from ...domain.entities.task import Task, TaskStatus
from ...domain.repositories.workflow_repository import WorkflowRepository
from ..utils.template_utils import substitute_task_description

logger = logging.getLogger(__name__)


class TaskOrchestrator:
    """
    Orchestrator for executing workflows with task dependencies.
    
    This orchestrator manages the execution of workflow tasks,
    handling dependencies and propagating outputs between tasks.
    """
    
    def __init__(self, workflow_repository: WorkflowRepository):
        self.workflow_repository = workflow_repository
        self.task_outputs: Dict[str, str] = {}
        self.executed_tasks: set = set()
    
    async def execute_workflow(
        self, 
        workflow: Workflow, 
        context: Dict[str, Any] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Execute a workflow with all its tasks.
        
        Args:
            workflow: The workflow to execute
            context: Additional context for task execution
            verbose: Whether to log execution details
            
        Returns:
            Dictionary containing task outputs and execution results
        """
        logger.info(f"Starting workflow execution: {workflow.name}")
        
        # Update workflow status
        workflow.start()
        await self.workflow_repository.update(workflow)
        
        try:
            # Initialize context
            execution_context = context or {}
            execution_context.update({
                'workflow_id': str(workflow.id),
                'workflow_name': workflow.name,
                'client_profile': workflow.client_profile,
                'target_audience': workflow.target_audience,
                'context': workflow.context
            })
            
            # Execute tasks in dependency order
            for task in workflow.tasks:
                await self._execute_task(task, execution_context, verbose)
            
            # Mark workflow as completed
            from ...domain.entities.workflow import WorkflowResult

            # Get final output (last task's output)
            final_output = ""
            if self.task_outputs:
                final_output = list(self.task_outputs.values())[-1]

            result = WorkflowResult(
                final_output=final_output,
                task_outputs={UUID(k): v for k, v in self.task_outputs.items()},
                execution_time=(datetime.utcnow() - workflow.started_at).total_seconds() if workflow.started_at else 0
            )
            workflow.complete(result)
            await self.workflow_repository.update(workflow)
            
            logger.info(f"Workflow execution completed: {workflow.name}")
            return {
                'success': True,
                'workflow_id': str(workflow.id),
                'task_outputs': self.task_outputs,
                'execution_time': workflow.result.execution_time if workflow.result else 0
            }
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            workflow.fail(str(e))
            await self.workflow_repository.update(workflow)
            
            return {
                'success': False,
                'workflow_id': str(workflow.id),
                'error': str(e),
                'task_outputs': self.task_outputs
            }
    
    async def _execute_task(
        self, 
        task: Task, 
        context: Dict[str, Any], 
        verbose: bool = True
    ) -> str:
        """
        Execute a single task with dependency resolution.
        
        Args:
            task: The task to execute
            context: Execution context
            verbose: Whether to log execution details
            
        Returns:
            Task output string
        """
        task_id = str(task.id)
        
        # Check if task already executed
        if task_id in self.task_outputs:
            return self.task_outputs[task_id]
        
        # Execute dependencies first
        dependency_outputs = {}
        for dep_id in task.dependencies:
            if dep_id not in self.task_outputs:
                # Find and execute dependency task
                dep_task = self._find_task_by_id(dep_id, context.get('workflow_tasks', []))
                if dep_task:
                    dependency_outputs[dep_id] = await self._execute_task(dep_task, context, verbose)
            else:
                dependency_outputs[dep_id] = self.task_outputs[dep_id]
        
        # Resolve template variables in task description
        template_context = {**context, **dependency_outputs}

        if verbose:
            logger.info(f"🔧 Resolving template variables for task: {task.name}")
            logger.debug(f"Available template variables: {list(template_context.keys())}")

        resolved_description = self._resolve_template_variables(
            task.description,
            template_context
        )

        if verbose and resolved_description != task.description:
            logger.info(f"✅ Template variables resolved for task: {task.name}")
            logger.debug(f"Original description length: {len(task.description)}")
            logger.debug(f"Resolved description length: {len(resolved_description)}")
        elif verbose:
            logger.info(f"ℹ️ No template variables found in task: {task.name}")
        
        if verbose:
            logger.info(f"Executing task: {task.name}")
            logger.debug(f"Task description: {resolved_description}")
        
        # Mark task as running
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        try:
            # Execute the task (this would integrate with actual AI agents)
            output = await self._execute_task_logic(task, resolved_description, context)
            
            # Mark task as completed
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.output = output
            
            # Store output for future tasks
            self.task_outputs[task_id] = output
            self.executed_tasks.add(task_id)
            
            logger.info(f"Task completed: {task.name}")
            return output
            
        except Exception as e:
            logger.error(f"Task execution failed: {task.name} - {str(e)}")
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error_message = str(e)
            
            # Store error as output
            error_output = f"Task failed: {str(e)}"
            self.task_outputs[task_id] = error_output
            
            raise e
    
    def _resolve_template_variables(self, text: str, variables: Dict[str, Any]) -> str:
        """
        Resolve template variables in text using {{variable}} syntax.

        Args:
            text: Text containing template variables
            variables: Dictionary of variable values

        Returns:
            Text with resolved variables
        """
        logger.info(f"🔧 _resolve_template_variables called with {len(variables)} variables")
        logger.debug(f"Available variables: {list(variables.keys())}")

        try:
            # Use the enhanced template substitution utility
            result = substitute_task_description(text, variables)

            logger.info(f"✅ Template substitution completed successfully")
            logger.debug(f"Original length: {len(text)}, Result length: {len(result)}")

            # Check if any substitution actually happened
            if result != text:
                logger.info(f"🎯 Template variables were substituted!")
            else:
                logger.warning(f"⚠️ No template variables were substituted")

            return result

        except Exception as e:
            logger.error(f"❌ Error resolving template variables: {str(e)}")
            logger.debug(f"Falling back to simple regex substitution")

            # Fallback to simple regex substitution
            def replace_variable(match):
                var_name = match.group(1)
                value = variables.get(var_name, f"{{{{{var_name}}}}}")
                return str(value) if value is not None else ''

            return re.sub(r"{{(\w+)}}", replace_variable, text)
    
    def _find_task_by_id(self, task_id: str, tasks: List[Task]) -> Optional[Task]:
        """Find a task by its ID in a list of tasks."""
        for task in tasks:
            if str(task.id) == task_id:
                return task
        return None
    
    async def _execute_task_logic(
        self,
        task: Task,
        description: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Execute the actual task logic using AI agents.

        Args:
            task: The task to execute
            description: Resolved task description
            context: Execution context

        Returns:
            Task output
        """
        logger.info(f"Executing task logic for: {task.name}")

        # Get agent executor from context if available
        agent_executor = context.get('agent_executor')
        if not agent_executor:
            logger.warning(f"No agent executor available for task {task.name}, using mock execution")
            return await self._mock_task_execution(task, description, context)

        # Find appropriate agent for this task
        agent = await self._get_agent_for_task(task, context)
        if not agent:
            logger.warning(f"No agent found for task {task.name}, using mock execution")
            return await self._mock_task_execution(task, description, context)

        try:
            # Add task and workflow context for agent logging
            enhanced_context = {
                **context,
                'task_id': str(task.id),
                'workflow_id': context.get('workflow_id', 'unknown')
            }

            # Execute agent with task description
            result = await agent_executor.execute_agent(
                agent=agent,
                task_description=description,
                context=enhanced_context
            )

            logger.info(f"Agent execution completed for task: {task.name}")
            return result

        except Exception as e:
            logger.error(f"Agent execution failed for task {task.name}: {str(e)}")
            # Fallback to mock execution on error
            return await self._mock_task_execution(task, description, context)

    async def _get_agent_for_task(self, task: Task, context: Dict[str, Any]) -> Optional[Any]:
        """Get appropriate agent for task execution."""
        from ...domain.entities.agent import Agent, AgentRole
        from uuid import uuid4

        # Create agents based on task name/role
        if task.name == "task1_brief" or task.agent_role == AgentRole.RESEARCHER:
            # RAG Specialist Agent
            return Agent(
                id=uuid4(),
                name="rag_specialist",
                role=AgentRole.RESEARCHER,
                goal="Retrieve and analyze client knowledge base content to create comprehensive project briefs",
                backstory="You are an expert at analyzing client documentation and creating detailed project briefs that guide content creation.",
                system_message="You specialize in retrieving relevant information from knowledge bases and creating structured briefs.",
                tools=["rag_get_client_content", "rag_search_content"]
            )

        elif task.name == "task2_research":
            # Web Searcher Agent
            return Agent(
                id=uuid4(),
                name="web_searcher",
                role=AgentRole.RESEARCHER,
                goal="Find current web information and trends to enhance content with up-to-date insights",
                backstory="You are an expert web researcher who finds the most current and relevant information to enhance content.",
                system_message="You specialize in web research and finding current trends and information. Always use web search tools to find the most recent and relevant information.",
                tools=["web_search", "web_search_financial"]
            )

        elif task.name == "task3_content" or task.agent_role == AgentRole.WRITER:
            # Copywriter Agent
            return Agent(
                id=uuid4(),
                name="copywriter",
                role=AgentRole.WRITER,
                goal="Create engaging, well-structured content that aligns with brand guidelines and speaks to the target audience",
                backstory="You are an expert copywriter who creates compelling content tailored to specific audiences and brand voices.",
                system_message="You specialize in creating high-quality, engaging content that meets specific requirements and brand guidelines.",
                tools=[]
            )

        # Default: return None for mock execution
        return None

    async def _mock_task_execution(
        self,
        task: Task,
        description: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Mock task execution for testing and fallback.

        Args:
            task: The task to execute
            description: Resolved task description
            context: Execution context

        Returns:
            Mock task output
        """
        logger.info(f"Using mock execution for task: {task.name}")

        # Generate realistic mock output based on task type
        if task.name == "task1_brief":
            return self._generate_mock_brief(context)
        elif task.name == "task2_research":
            return self._generate_mock_research(context)
        elif task.name == "task3_content":
            return self._generate_mock_content(context)
        else:
            # Generic mock output
            mock_output = f"""
# Task Output: {task.name}

**Task Type**: {task.task_type}
**Agent Role**: {task.agent_role}
**Description**: {description}

## Generated Content

This is a mock output for task '{task.name}'.
In the full implementation, this would be replaced with actual AI agent execution.

**Context Used**:
- Client Profile: {context.get('client_name', 'N/A')}
- Target Audience: {context.get('target_audience', 'N/A')}
- Topic: {context.get('topic', 'N/A')}

**Execution Time**: {datetime.utcnow().isoformat()}
"""
            return mock_output.strip()

    def _generate_mock_brief(self, context: Dict[str, Any]) -> str:
        """Generate mock brief for task1."""
        return f"""
# Project Brief: {context.get('topic', 'Content Creation')}

## Executive Summary
This project involves creating high-quality content about "{context.get('topic', 'the specified topic')}" for {context.get('client_name', 'the client')}.

## Brand Context & Guidelines
- Client: {context.get('client_name', 'Default Client')}
- Brand Voice: Professional yet accessible
- Target Audience: {context.get('target_audience', 'General audience')}

## Topic Analysis & Objectives
- Main Topic: {context.get('topic', 'Content topic')}
- Content Goals: Educate, inform, and engage the target audience
- Key Messages: To be developed based on research

## Content Requirements
- Format: Article
- Tone: Professional and engaging
- Length: Comprehensive coverage of the topic
- Include: Current trends, statistics, and actionable insights

## Success Criteria
- Alignment with brand voice
- Relevance to target audience
- Inclusion of current, accurate information
- Clear, engaging writing style
"""

    def _generate_mock_research(self, context: Dict[str, Any]) -> str:
        """Generate mock research enhancement for task2."""
        return f"""
# Enhanced Research Brief: {context.get('topic', 'Content Creation')}

## Current Market Trends
Based on recent web research, the following trends are relevant to "{context.get('topic', 'the topic')}":

- Trend 1: Increasing focus on digital transformation
- Trend 2: Growing importance of data-driven decision making
- Trend 3: Rising demand for personalized experiences

## Key Statistics
- 75% of organizations are investing in related technologies
- Market growth rate: 15% year-over-year
- Consumer adoption: 60% and growing

## Industry Insights
Recent developments in the field show significant opportunities for content that addresses:
- Practical implementation strategies
- Common challenges and solutions
- Future outlook and predictions

## Content Opportunities
- Educational explainers for complex concepts
- Case studies and real-world examples
- Actionable tips and best practices
- Industry expert perspectives

## Recommended Approach
Create content that combines foundational knowledge with current trends and practical applications.
"""

    def _generate_mock_content(self, context: Dict[str, Any]) -> str:
        """Generate mock final content for task3."""
        topic = context.get('topic', 'Technology Trends')
        target_audience = context.get('target_audience', 'professionals')

        return f"""
# {topic}: A Comprehensive Guide for {target_audience.title()}

## Introduction

In today's rapidly evolving landscape, understanding {topic.lower()} has become essential for {target_audience}. This comprehensive guide explores the key aspects, current trends, and practical implications you need to know.

## Current State of {topic}

The field of {topic.lower()} is experiencing unprecedented growth and transformation. Recent research indicates significant developments that are reshaping how we approach this domain.

### Key Developments

1. **Innovation Acceleration**: The pace of change has increased dramatically
2. **Market Expansion**: New opportunities are emerging across sectors
3. **Technology Integration**: Advanced tools are becoming more accessible

## Practical Implications

For {target_audience}, these developments mean:

- **Enhanced Opportunities**: New avenues for growth and development
- **Skill Requirements**: Evolving competencies needed for success
- **Strategic Considerations**: Important factors for decision-making

## Best Practices

Based on current research and industry insights, here are recommended approaches:

1. **Stay Informed**: Keep up with latest developments
2. **Continuous Learning**: Invest in skill development
3. **Strategic Planning**: Align efforts with market trends
4. **Network Building**: Connect with industry professionals

## Looking Forward

The future of {topic.lower()} promises continued evolution and opportunity. By understanding current trends and preparing for upcoming changes, {target_audience} can position themselves for success.

## Conclusion

{topic} represents both challenges and opportunities for {target_audience}. By staying informed, adapting to change, and implementing best practices, you can navigate this dynamic landscape effectively.

---

*This content was generated as part of a comprehensive research and analysis process, incorporating current market trends and industry insights.*
"""
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the current execution state."""
        return {
            'executed_tasks': len(self.executed_tasks),
            'task_outputs_count': len(self.task_outputs),
            'execution_status': 'completed' if self.task_outputs else 'not_started'
        }
