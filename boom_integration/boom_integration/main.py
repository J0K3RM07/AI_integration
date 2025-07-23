from fastapi import FastAPI
from boom_integration.models import QuestionRequest
from boom_integration.ai_client import OpenAIClient, AIClient
from boom_integration.recognizers import YoloRecognizer, Recognizer
from ultralytics import YOLO
from contextlib import asynccontextmanager
from fastapi import Request
from boom_integration.db import engine, create_tables, AnalyzeLog
from boom_integration.repositories import AnalyzeLogRepository
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:123qweloL@localhost:5432/postgres"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.yolo_model = YOLO("yolo11n.pt")
    await create_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/analyze")
async def analyze_service(data: QuestionRequest, request: Request):
    model = request.app.state.yolo_model
    recognizer: Recognizer = YoloRecognizer(model)
    detected_objects = recognizer.recognize(data.base64)
    ai_client: AIClient = OpenAIClient()
    llm_response = ai_client.ask(data.question, detected_objects)
    await AnalyzeLogRepository.add_log(data.question, detected_objects, llm_response)
    return {"detected_objects": detected_objects, "llm_response": llm_response}


@app.get("/logs")
async def get_logs():
    logs = await AnalyzeLogRepository.get_logs()
    return [
        {
            "id": log.id,
            "question": log.question,
            "detected_objects": log.detected_objects,
            "llm_response": log.llm_response,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
