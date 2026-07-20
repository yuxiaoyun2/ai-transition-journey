from agents import Runner

from app.agents.task_agent import task_agent


class AgentService:
    async def chat(self, message: str) -> str:
        result = await Runner.run(
            starting_agent=task_agent,
            input=message,
        )

        return result.final_output
