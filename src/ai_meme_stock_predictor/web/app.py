from fastapi import FastAPI, Body
from pydantic import BaseModel
from ..agent.portia_agent import PortiaMemeAgent
from ..utils.logging_setup import init_logging

init_logging()
app = FastAPI(title="AI Meme Stock Predictor")
agent = PortiaMemeAgent()

class Query(BaseModel):
    conversation_id: str
    text: str

@app.post("/query")
async def query(payload: Query):
    result = agent.handle_query(payload.conversation_id, payload.text)
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}
