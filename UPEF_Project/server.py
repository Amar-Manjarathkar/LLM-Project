# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Import your existing modules without changing them
# Ensure folders are set up as: src/models/engine.py and src/cleaning/cleaner.py
from src.cleaning.cleaner import IntelCleaner
from src.models.engine import IntelligenceEngine

app = FastAPI()

# Initialize your components
# Make sure the Ollama model is pulled on cn14 before running this
import platform

cleaner = IntelCleaner()
# UPGRADED to 32b model for gpu39
engine = IntelligenceEngine(model_name="qwen2.5:32b")

class RequestData(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": f"Backend is running on {platform.node()}", "model": "qwen2.5:32b"}

@app.post("/analyze")
def run_analysis(data: RequestData):
    """
    Takes raw text, cleans it, runs the engine, and returns the JSON report.
    """
    try:
        # 1. Clean the text using your existing cleaner
        cleaned_text = cleaner.process(data.text)

        # 2. Run your existing engine
        # The engine returns a Pydantic object (IntelReport), which FastAPI handles automatically
        report = engine.analyze(cleaned_text)

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 is crucial to allow connections from the tunnel
    uvicorn.run(app, host="0.0.0.0", port=8000)