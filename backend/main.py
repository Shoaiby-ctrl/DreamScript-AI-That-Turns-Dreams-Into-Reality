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

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to frontend folder (adjust if needed)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)

# Mount the whole frontend folder as /static
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))


# --- API endpoint ---
from pydantic import BaseModel

class DreamRequest(BaseModel):
    dream: str
    constraints: str | None = None

@app.post("/generate")
async def generate(request: DreamRequest):
    # Use Gemini
    prompt = f"Dream: {request.dream}\nConstraints: {request.constraints or 'None'}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {"result": response.text}
