from app.clients.together import TogetherService
from fastapi import HTTPException
from loguru import logger

class ChatService:
    def __init__(self, together: TogetherService):
        "tao server xu ly hoi thoai"
        self.together = together

    async def chat(self, text: str) -> str:
        "gui yc den together"
        try:
            return await self.together.chat(text)
        except Exception as e:
            logger.error(f"loi chat: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        