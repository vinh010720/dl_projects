from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TextRequest, APIResponse, ConversationResult
from app.services.chat import ChatService
from app.clients.together import TogetherService
from loguru import logger

router = APIRouter(prefix="/chat", tags=["chat"])

def get_together_service() -> TogetherService:
    return TogetherService()

def get_chat_service(together: TogetherService = Depends(get_together_service)) -> ChatService:
    return ChatService(together)

@router.post("/", response_model=APIResponse)
async def chat_endpoint(
    request: dict,  # Đổi từ TextRequest thành dict
    chat_service: ChatService = Depends(get_chat_service)
):
    try:
        # Chuyển đổi dict thành object Pydantic
        request_obj = TextRequest(**request)  # <-- Fix lỗi
        reply = await chat_service.chat(request_obj.text)
        return APIResponse(
            status="success",
            data=ConversationResult(
                response=reply,
                context=[(request_obj.text, reply)]
            )
        )
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Chat endpoint error")
    