import io
import json
from openai import AsyncOpenAI, APIError
from loguru import logger
from app.config import settings

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def transcribe(self, audio: bytes, file_format: str, language: str) -> str:
        try:
            audio_file = io.BytesIO(audio)
            audio_file.name = f"audio.{file_format}"
            
            response = await self.client.audio.transcriptions.create(
                model=settings.whisper_model,
                file=audio_file,
                language=language
            )
            return response.text
        except APIError as e:
            logger.error(f"OpenAI API Error: {e}", exc_info=True)
            raise ValueError(f"Transcription error: {e.message}")
        except Exception as e:
            logger.error(f"Transcription failed: {str(e)}", exc_info=True)
            raise ValueError("Audio processing error")

    async def evaluate(self, text: str) -> dict:
        try:
            prompt = f"""
Đánh giá bài nói theo các tiêu chí:
1. Phát âm (pronunciation): float (0-10)
2. Độ trôi chảy (fluency): float (0-10)
3. Ngữ pháp (grammar): float (0-10)
4. Gợi ý cải thiện (feedback): list[string] (ít nhất 3 mục)

Yêu cầu:
- Định dạng đầu ra JSON nghiêm ngặt
- Làm tròn điểm số đến 1 chữ số thập phân
- Gợi ý cụ thể và mang tính xây dựng

Nội dung cần đánh giá: "{text}"

Kết quả JSON phải theo mẫu:
{{
    "pronunciation": 8.5,
    "fluency": 7.0,
    "grammar": 9.0,
    "feedback": [
        "Gợi ý 1",
        "Gợi ý 2",
        "Gợi ý 3"
    ]
}}
"""

            response = await self.client.chat.completions.create(
                model=settings.gpt_eval_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=1000
            )

            response_text = response.choices[0].message.content.strip()
            logger.debug(f"Raw OpenAI response: {response_text}")

            # Xử lý response nhiều định dạng
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("Invalid JSON format in response")
                
            clean_json = response_text[json_start:json_end]

            try:
                parsed = json.loads(clean_json)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode failed. Content: {clean_json}")
                raise ValueError(f"Invalid JSON response: {str(e)}")

            # Validate nghiêm ngặt
            required_fields = {
                "pronunciation": (float, int),
                "fluency": (float, int),
                "grammar": (float, int),
                "feedback": list
            }

            for field, types in required_fields.items():
                if field not in parsed:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(parsed[field], types):
                    raise ValueError(f"Invalid type for {field}. Expected {types}")

            if len(parsed["feedback"]) < 3:
                raise ValueError("At least 3 feedback items required")

            # Convert các giá trị số về float
            parsed["pronunciation"] = float(parsed["pronunciation"])
            parsed["fluency"] = float(parsed["fluency"])
            parsed["grammar"] = float(parsed["grammar"])

            return parsed

        except APIError as e:
            logger.error(f"OpenAI API failure: {e}")
            raise ValueError("Evaluation service unavailable")
        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}", exc_info=True)
            raise ValueError("Failed to process evaluation")