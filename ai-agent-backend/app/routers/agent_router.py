from fastapi import APIRouter, Depends

from app.schemas.agent_schema import (
    AgentChatRequest,
    AgentChatResponse,
)

from app.services.agent_service import AgentService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


def get_agent_service() -> AgentService:
    return AgentService()


@router.post(
    "/chat",
    response_model=AgentChatResponse,
)
async def chat_with_agent(
    request: AgentChatRequest, service: AgentService = Depends(get_agent_service)
) -> AgentChatResponse:
    answer = await service.chat(request.message)

    return AgentChatResponse(answer=answer)
