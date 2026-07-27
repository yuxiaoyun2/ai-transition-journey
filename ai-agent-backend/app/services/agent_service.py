from agents import Runner

from app.agents.task_agent import task_agent
from app.exceptions.task_exceptions import AIServiceError
from app.agents.agent_context import AgentContext
from app.schemas.agent_schema import SearchResult

import logging

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(self, message: str, session_id: str) -> SearchResult:
        try:
            context = AgentContext(
                session_id=session_id,
            )
            result = await Runner.run(
                starting_agent=task_agent, input=message, context=context
            )

            data: SearchResult = result.final_output
            return data
        except Exception:
            logger.exception(
                "Agent execution failed: session_id=%s",
                session_id,
            )
            raise AIServiceError()
