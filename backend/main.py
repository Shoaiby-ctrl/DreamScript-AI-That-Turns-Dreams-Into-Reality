from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv  # ✅ Load .env file

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("❌ No GEMINI_API_KEY found in .env")

# --- Gemini setup ---
import google.generativeai as genai
genai.configure(api_key=api_key)

app = FastAPI()

# ✅ CORS Configuration
# Change the second URL after you deploy frontend on Vercel
origins = [
    "http://localhost:3000",             # Local frontend (React/Next.js dev)
    "https://YOUR-VERCEL-APP.vercel.app" # Replace with actual Vercel domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve Frontend (optional, if needed) ---
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

# Serve static files from frontend
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    """Serves the frontend index.html if available"""
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend not found. Did you build it?"}

# --- API endpoint ---
from pydantic import BaseModel

class DreamRequest(BaseModel):
    dream: str
    constraints: str | None = None

@app.post("/generate")
async def generate(request: DreamRequest):
    """Generates dream content using Gemini API"""
    prompt = f"Dream: {request.dream}\nConstraints: {request.constraints or 'None'}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {"result": response.text}
