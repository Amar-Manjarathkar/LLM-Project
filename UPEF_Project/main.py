# Entry point for the pipeline

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import our custom modules
from src.cleaning.cleaner import IntelCleaner
from src.models.engine import IntelligenceEngine
from src.models.schemas import IntelReport

# Initialize the App
app = FastAPI(
    title="UPEF Intelligence API",
    description="API for classifying Indian Context Intel (Language, Domain, NER)",
    version="1.0.0"
)

# Initialize Components (Load Model Once on Startup)
print("🚀 Loading Intelligence Engine...")
cleaner = IntelCleaner()
engine = IntelligenceEngine(model_name="qwen2.5:7b")
print("✅ Engine Loaded.")

# Define Request Body
class IntelRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Online", "model": "qwen2.5:7b"}

@app.post("/analyze", response_model=IntelReport)
def analyze_intel(payload: IntelRequest):
    """
    Endpoint to process raw text and return Intelligence Report.
    """
    try:
        # 1. Clean
        cleaned_text = cleaner.process(payload.text)
        
        # 2. Analyze
        report = engine.analyze(cleaned_text)
        
        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the API server on localhost:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)