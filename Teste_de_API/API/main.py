from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for searching healthcare operators in Brazil",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(routes.router, prefix="/api/v1", tags=["operators"])
