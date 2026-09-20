from fastapi import FastAPI

from backend.app.api.predict import (
    router as predict_router,
)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title=(
        "AI-Based Waste Segregation and "
        "Microbial Decomposition API"
    ),
    description=(
        "Backend API for waste image classification "
        "and evidence-backed microbial decomposition "
        "recommendations."
    ),
    version="0.1.0",
)


# ============================================================
# Routers
# ============================================================

app.include_router(
    predict_router
)


# ============================================================
# Health Check
# ============================================================

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok",
        "service": "waste-segregation-api",
        "version": "0.1.0",
    }
