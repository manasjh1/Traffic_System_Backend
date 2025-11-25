from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all API routes
from api.detect import router as detect_router
from api.logs import router as logs_router
from api.stats import router as stats_router

app = FastAPI(
    title="College Traffic Monitoring System (CTMS)",
    description="Backend API for vehicle detection, OCR, and traffic violation logging",
    version="1.0.0"
)

# -----------------------------
# Enable CORS (required for frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers
)

# -----------------------------
# Register Routes
# -----------------------------
app.include_router(detect_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

# -----------------------------
# Root route
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "CTMS Backend Running Successfully 🚀",
        "endpoints": {
            "/api/detect/": "Run YOLO + EasyOCR detection",
            "/api/logs/": "Fetch traffic logs",
            "/api/stats/": "Dashboard statistics"
        }
    }
