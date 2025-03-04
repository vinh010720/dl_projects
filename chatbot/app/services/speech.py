from fastapi import HTTPException
from app.clients.openai import OpenAIService
from loguru import logger

class SpeechService:
    def __init__(self, openai: OpenAIService):
        "process audio"
        self.openai = openai   

    
    async def transcribe(self, audio: bytes, file_format: str, language: str) -> str:
        "STT use Whisper"
        try:
            transcript =  await self.openai.transcribe(audio, file_format, language)
            return transcript
        except Exception as e: 
            logger.error(f"error convert audio: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="audio conversion service failed, pls try again later")
