from fastapi import FastAPI


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
    version="0.1.0"
)


# ============================================================
# Health Check
# ============================================================

@app.get(
    "/health",
    tags=["Health"]
)
def health_check():
    """
    Check whether the backend API is running.
    """

    return {
        "status": "ok",
        "service": "waste-segregation-api",
        "version": "0.1.0"
    }