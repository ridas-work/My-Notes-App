from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine, Base
from app.routers import notes, tags, auth
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Note Taking API",
    description="A simple API for managing notes with tags and user authentication",
    version="2.0.0"
)

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(tags.router)

# Startup event
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🚀 Note Taking API Server Started Successfully!")
    print("="*60)
    print(f"📝 Web Interface:    http://127.0.0.1:8000/")
    print(f"📚 API Docs:         http://127.0.0.1:8000/docs")
    print(f"🔐 Login Page:       http://127.0.0.1:8000/login")
    print(f"📋 Register Page:    http://127.0.0.1:8000/register")
    print("="*60 + "\n")

# Root endpoint - Notes page (will check auth in JavaScript)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Register page
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# API root endpoint
@app.get("/api")
def api_root():
    return {
        "message": "Welcome to Note Taking API with Authentication",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Run server if executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
