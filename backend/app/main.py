from fastapi import FastAPI

app = FastAPI(
    title="AI Equity Research Platform",
    description="AI-powered Indian equity research and risk intelligence API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Equity Research API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }