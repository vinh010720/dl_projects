import asyncio
from together import Together
from app.config import settings

class TogetherService:
    def __init__(self):
        "Init together client"
        self.client = Together(api_key=settings.together_api_key)
        
    async def chat(self, text: str) -> str:
        "Chat with Llama"
        try: 
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=settings.llama_model,
                messages=[{"role": "user", "content": text}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
