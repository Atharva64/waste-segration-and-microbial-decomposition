from fastapi import FastAPI

from backend.app.api.history import router as history_router
from backend.app.api.predict import router as predict_router
from backend.app.api.waste import router as waste_router
from backend.app.core.error_handlers import register_exception_handlers


app = FastAPI(
    title="AI-Based Waste Segregation and Microbial Decomposition API",
    description=(
        "Backend API for waste image classification and evidence-backed "
        "microbial decomposition recommendations."
    ),
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(predict_router)
app.include_router(waste_router)
app.include_router(history_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "waste-segregation-api",
        "version": "0.1.0",
    }
