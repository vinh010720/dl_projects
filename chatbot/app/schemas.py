from pydantic import BaseModel, Field
from typing import Literal, Optional, Union, List, Tuple

class BaseRequest(BaseModel):
    language: Optional[Literal['en','vi']] = None

class SpeechRequest(BaseModel):
 
    file_format: str = "webm"  # thêm trường file_format
    language: Optional[Literal['en','vi']] = None

class TextRequest(BaseRequest):
    text: str = Field(..., alias="prompt")
    history: List[Tuple[Optional[str], Optional[str]]] = []
    
    class Config:
        populate_by_name = True  # Cho phép FastAPI map alias

 

class EvaluationResult(BaseModel):
    transcript: str
    pronunciation: float
    fluency: float
    grammar: float
    feedback: List[str]

class ConversationResult(BaseModel):
    response: str
    context: List[Tuple[str, str]]

class APIResponse(BaseModel):
    status: Literal["success", "error"]
    data: Optional[Union[EvaluationResult, ConversationResult]] = None
    error: Optional[str] = None
