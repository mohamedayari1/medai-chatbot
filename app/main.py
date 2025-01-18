from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



# from app.core.config import settings
from app.routes import answer

app = FastAPI(
    title="LawGPT API",
    description="API for LawGPT - A Legal Question Answering System",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(answer.router, tags=["answer"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to LawGPT API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
