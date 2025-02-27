from fastapi import FastAPI, Request    
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os 

from .models import ChatRequest
from together import Together
from .chat_handler import get_chat_response  
from fastapi.staticfiles import StaticFiles



load_dotenv()
TOGETHER_API_KEY = os.getenv("together_api_key")

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),  # <-- Sửa đường dẫn
    name="static"
)


client = Together(api_key=TOGETHER_API_KEY)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint /chat nhận vào 1 prompt và (tùy chọn) history dưới dạng list các tuple (user, bot).
    Xây dựng context và gọi API Together AI để trả về câu trả lời.
    """
    try:
        response_text = get_chat_response(client, request.prompt, request.history)
        return {"response": response_text}
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",port=8000)