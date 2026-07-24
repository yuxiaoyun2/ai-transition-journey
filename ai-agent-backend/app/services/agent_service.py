from agents import Runner

from app.agents.task_agent import task_agent
from app.exceptions.task_exceptions import AIServiceError


class AgentService:
    async def chat(self, message: str) -> str:
        try:
            result = await Runner.run(
                starting_agent=task_agent,
                input=message,
            )

            return result.final_output
        except Exception:
            raise AIServiceError()
