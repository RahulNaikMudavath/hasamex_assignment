import os
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.parser import (
    load_case_pack_transcripts,
    parse_transcript_text,
    ParsedTranscript
)
from backend.interview_guide import get_complete_interview_guide_analysis
from backend.synthesis import generate_cross_call_synthesis
from backend.qa_engine import QAEngine, QAResponse
from backend.verifier import verify_quote_in_transcript

app = FastAPI(
    title="CallSynth AI – Expert Call Analysis Engine",
    description="Hasamex Technical Case Study: European Robotic Surgery Market Analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASE_PACK_DIR = os.path.join(BASE_DIR, "case_pack")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# In-memory store
transcripts_store: Dict[str, ParsedTranscript] = {}
qa_engine: Optional[QAEngine] = None

def init_app():
    global transcripts_store, qa_engine
    transcripts_store = load_case_pack_transcripts(CASE_PACK_DIR)
    qa_engine = QAEngine(transcripts_store)

init_app()

class QueryRequest(BaseModel):
    query: str
    api_key: Optional[str] = None
    provider: Optional[str] = "auto"
    market_filter: Optional[str] = None

class QuoteVerifyRequest(BaseModel):
    quote: str
    transcript_id: str

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "loaded_transcripts": len(transcripts_store),
        "transcript_ids": list(transcripts_store.keys())
    }

@app.get("/api/transcripts")
def get_transcripts():
    return {
        "count": len(transcripts_store),
        "transcripts": [
            {
                "metadata": t.metadata.model_dump(),
                "turns": [turn.model_dump() for turn in t.turns],
                "raw_text": t.raw_text
            }
            for t in transcripts_store.values()
        ]
    }

@app.get("/api/transcripts/{transcript_id}")
def get_single_transcript(transcript_id: str):
    if transcript_id not in transcripts_store:
        raise HTTPException(status_code=404, detail="Transcript not found")
    t = transcripts_store[transcript_id]
    return {
        "metadata": t.metadata.model_dump(),
        "turns": [turn.model_dump() for turn in t.turns],
        "raw_text": t.raw_text
    }

@app.get("/api/interview-guide")
def get_interview_guide():
    analysis = get_complete_interview_guide_analysis(transcripts_store)
    return {
        "total_questions": len(analysis),
        "analysis": [q.model_dump() for q in analysis]
    }

@app.get("/api/synthesis")
def get_synthesis():
    synth = generate_cross_call_synthesis()
    return synth.model_dump()

@app.post("/api/qa")
def ask_question(req: QueryRequest):
    if not qa_engine:
        raise HTTPException(status_code=500, detail="QA Engine not initialized")
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    response = qa_engine.answer_query(
        query=req.query,
        api_key=req.api_key,
        provider=req.provider or "auto"
    )
    return response.model_dump()

@app.post("/api/verify-quote")
def verify_quote(req: QuoteVerifyRequest):
    if req.transcript_id not in transcripts_store:
        raise HTTPException(status_code=404, detail="Transcript not found")
    t = transcripts_store[req.transcript_id]
    res = verify_quote_in_transcript(req.quote, t.raw_text, t.turns)
    return res.model_dump()

class TranscriptUploadRequest(BaseModel):
    filename: str
    content: str

@app.post("/api/upload-transcript")
async def upload_transcript(req: TranscriptUploadRequest):
    global qa_engine
    try:
        raw_text = req.content
        parsed = parse_transcript_text(raw_text, filename=req.filename or "custom_transcript.txt")
        transcripts_store[parsed.metadata.id] = parsed
        qa_engine = QAEngine(transcripts_store)
        return {
            "message": f"Successfully parsed and loaded {req.filename}",
            "transcript_id": parsed.metadata.id,
            "metadata": parsed.metadata.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse uploaded transcript: {str(e)}")

@app.post("/api/reset-transcripts")
def reset_transcripts():
    init_app()
    return {"message": "Reset to 3 default case pack transcripts.", "count": len(transcripts_store)}

# Static files
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(content={"message": "CallSynth AI API Running. Please create static/index.html"})

if __name__ == "__main__":
    import uvicorn
    print("Starting CallSynth AI application on http://localhost:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
