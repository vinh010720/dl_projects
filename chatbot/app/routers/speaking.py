# app/routers/speaking.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.schemas import APIResponse, EvaluationResult
from app.services.speech import SpeechService
from app.services.evaluation import EvaluationService
from app.dependencies import get_speech_service, get_evaluation_service
from loguru import logger

router = APIRouter(prefix="/speaking", tags=["Speaking"])

@router.post("/evaluate", response_model=APIResponse)
async def evaluate_speech(
    audio: UploadFile = File(...),
    language: str = Form(...),
    file_format: str = Form("webm"),
    speech_service = Depends(get_speech_service),
    eval_service = Depends(get_evaluation_service)
):
    try:
        audio_bytes = await audio.read()
        transcript = await speech_service.transcribe(audio_bytes, file_format, language)
        evaluation = await eval_service.evaluate(transcript)
        return APIResponse(status="success", data=evaluation)
    except Exception as e:
        logger.error(f"Speaking endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Speaking endpoint error")
