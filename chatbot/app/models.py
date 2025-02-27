from pydantic import BaseModel
from typing import List, Tuple, Optional

class ChatRequest(BaseModel):
    prompt: str
    history: Optional[List[Tuple[str, str]]] = []
    