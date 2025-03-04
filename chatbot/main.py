from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routers import chat, speaking
from app.utils.logging import configure_logging

app = FastAPI(title="AAA")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Cấu hình logging
configure_logging()

# Mount thư mục chứa file tĩnh (CSS, JS, hình ảnh)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cấu hình template (chuyển file HTML vào thư mục 'templates')
templates = Jinja2Templates(directory="templates")

# Route cho trang chủ, render file index.html từ thư mục templates
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Đăng ký các router API
app.include_router(chat.router)
app.include_router(speaking.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
