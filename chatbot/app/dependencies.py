from fastapi import Depends
from app.clients.openai import OpenAIService
from app.clients.together import TogetherService
from app.services.speech import SpeechService
from app.services.evaluation import EvaluationService
from app.services.chat import ChatService

def get_openai() -> OpenAIService:
    return OpenAIService()

def get_together() -> TogetherService:
    return TogetherService()

def get_speech_service(
    openai: OpenAIService = Depends(get_openai)
) -> SpeechService:
    return SpeechService(openai)

def get_evaluation_service(
    openai: OpenAIService = Depends(get_openai)
) -> EvaluationService:
    return EvaluationService(openai)

def get_chat_service(
    together: TogetherService = Depends(get_together)
) -> ChatService:
    return ChatService(together)
