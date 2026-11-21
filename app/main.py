from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.database import Base, engine
from app import models  # noqa: F401 - register SQLAlchemy models
from app.api.routes import auth, users, bmi, goals, settings as settings_routes, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the BMI Calculator Flutter application.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.api_v1_prefix
app.include_router(auth.router , prefix=prefix)
app.include_router(users.router, prefix=prefix)
app.include_router(bmi.router, prefix=prefix)
app.include_router(goals.router, prefix=prefix)
app.include_router(settings_routes.router, prefix=prefix)
app.include_router(dashboard.router, prefix=prefix)


@app.get("/", tags=["System"])
def root():
    return {"name": settings.app_name, "status": "running", "docs": "/docs"}


@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy"}

# run : python -m uvicorn app.main:app --reload