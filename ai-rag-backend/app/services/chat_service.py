from app.services.ai_service import AIService
from app.services.retrieval_service import RetrievalService
from app.schemas.search_schema import SearchItem
from app.schemas.chat_schema import ChatResponse

from textwrap import dedent

THRESHOLD = 0.9


class ChatService:
    def __init__(
        self,
        ai_service: AIService,
        retrieval_service: RetrievalService,
    ):
        self.ai_service = ai_service
        self.retrieval_service = retrieval_service

    def chat(self, question: str, top_k: int) -> ChatResponse:
        search_response = self.retrieval_service.search(question=question, top_k=top_k)

        if not search_response.results:
            return ChatResponse(
                answer="関連する情報は見つかりませんでした。",
                sources=[],
            )

        results = [
            item for item in search_response.results if item.distance <= THRESHOLD
        ]

        prompt = self.build_prompt(question=question, results=results)

        answer = self.ai_service.generate_chat(prompt=prompt)

        sources = self.get_sources(results)

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    def get_sources(
        self,
        results: list[SearchItem],
    ) -> list[str]:
        sources = []

        for item in results:
            title = item.metadata.title

            page_number = item.metadata.page_number

            if page_number is not None:
                source = f"{title} Page {page_number}"
            else:
                source = title

            sources.append(source)

        return list(dict.fromkeys(sources))

    def build_prompt(
        self,
        question: str,
        results: list[SearchItem],
    ) -> str:
        contexts = []
        for item in results:
            contexts.append(
                dedent(
                    f"""
                    Document:
                    {item.metadata.title}
            
                    Page:
                    {item.metadata.page_number}
            
                    Content:
                    {item.content}
                    """
                ).strip()
            )

        context = "\n\n=============\n\n".join(contexts)

        return dedent(
            f"""

            あなたは文書検索AIです。

            以下のContextのみを根拠として回答してください。

            Context以外の知識は使用しないでください。

            Contextに回答が存在しない場合は、

            「文書内には関連する情報が見つかりませんでした。」

            と回答してください。
            
            Context:
            {context}
            
            Question:
            {question}
            """
        ).strip()
