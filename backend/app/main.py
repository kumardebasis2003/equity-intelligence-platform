from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.research import router as research_router
from app.api.health import router as health_router


# ==========================================
# AI EQUITY INTELLIGENCE PLATFORM
# ==========================================

app = FastAPI(
    title="AI Equity Intelligence Platform",
    description=(
        "AI-powered equity research platform with "
        "market data, machine learning predictions, "
        "portfolio risk analysis, and RAG-based "
        "financial research."
    ),
    version="1.0.0",
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API ROUTERS
# ==========================================

# RAG research API
app.include_router(
    research_router
)

# RAG health API
app.include_router(
    health_router
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():

    return {
        "message": "AI Equity Intelligence Platform API",
        "status": "running",
        "version": "1.0.0",
    }


# ==========================================
# GENERAL HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "equity-intelligence-platform",
    }


# ==========================================
# API INFORMATION
# ==========================================

@app.get("/api")
def api_info():

    return {
        "name": "AI Equity Intelligence Platform",
        "version": "1.0.0",
        "modules": [
            "Market Data",
            "Technical Indicators",
            "XGBoost Predictions",
            "Backtesting",
            "Portfolio Risk Analysis",
            "RAG Research",
        ],
    }