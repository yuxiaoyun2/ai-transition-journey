from app.services.ai_service import AIService
from app.services.retrieval_service import RetrievalService
from app.schemas.search_schema import SearchResponse
from app.schemas.chat_schema import ChatResponse

from textwrap import dedent


class ChatService:
    def __init__(
        self,
        ai_service: AIService,
        retrieval_service: RetrievalService,
    ):
        self.ai_service = ai_service
        self.retrieval_service = retrieval_service

    def chat(
        self,
        question: str,
    ) -> ChatResponse:
        search_response = self.retrieval_service.search(question=question)

        if not search_response.results:
            return ChatResponse(
                answer="関連する情報は見つかりませんでした。",
                sources=[],
            )

        context = self.get_context(search_response)

        prompt = self.build_prompt(question=question, context=context)

        answer = self.ai_service.generate_chat(prompt=prompt)

        sources = self.get_sources(search_response)

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    def get_context(
        self,
        search_response: SearchResponse,
    ) -> str:
        return "\n\n".join(chunk.content for chunk in search_response.results)

    def get_sources(
        self,
        search_response: SearchResponse,
    ) -> list[str]:
        sources = []

        for item in search_response.results:
            metadata = item.metadata

            title = metadata.get(
                "title",
                "Unknown document",
            )

            page_number = metadata.get("page_number")

            if page_number is not None:
                source = f"{title} Page {page_number}"
            else:
                source = title

            sources.append(source)

        return list(dict.fromkeys(sources))

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        return dedent(
            f"""

            あなたは文書検索AIです。

            以下のContextのみを根拠として回答してください。
            Contextに回答がない場合は、推測せず、
            「文書内には関連する情報が見つかりませんでした。」
            と回答してください。

            Context:
            {context}

            Question:
            {question}
            """
        ).strip()
