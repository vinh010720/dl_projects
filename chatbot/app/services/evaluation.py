from fastapi import HTTPException
from app.clients.openai import OpenAIService
from app.schemas import EvaluationResult
from loguru import logger
from pydantic import ValidationError

class EvaluationService:
    def __init__(self, openai: OpenAIService):
        self.openai = openai
    
    async def evaluate(self, text: str) -> EvaluationResult:
        try:
            # Gọi OpenAI service để lấy kết quả đánh giá
            openai_result = await self.openai.evaluate(text)
            
            # Tạo dictionary với đầy đủ các trường cần thiết
            result_data = {
                "transcript": text,
                **openai_result  # Merge toàn bộ dữ liệu từ OpenAI
            }
            
            # Validate và trả về kết quả
            return EvaluationResult(**result_data)
            
        except ValidationError as e:
            logger.error(f"Validation error: {e.errors()}")
            raise HTTPException(
                status_code=422,
                detail={"message": "Invalid response format", "errors": e.errors()}
            )
        except ValueError as e:
            logger.error(f"Value error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Evaluation error: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")