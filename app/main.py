from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="Financial Fake News Detection API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fake-news-mauve.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)

@app.get("/")
def home():
    return {"message": "API is running 🚀"}