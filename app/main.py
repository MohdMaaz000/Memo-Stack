import time
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1.api import api_router
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

openapi_tags = [
    {
        "name": "auth",
        "description": "Operations with user authentication and token generation.",
    },
    {
        "name": "users",
        "description": "Operations with user accounts.",
    },
    {
        "name": "books",
        "description": "Manage books and collaborative reading.",
    },
    {
        "name": "notes",
        "description": "Manage structured notes associated with books.",
    },
    {
        "name": "comments",
        "description": "Peer comments on individual notes.",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME, 
    description="""
MemoStack is a high-performance **RESTful backend API** designed for structured note-taking and collaborative book annotations.

## 🚀 Features
* **JWT Authentication**: Secure endpoints using Access and Refresh tokens.
* **Books Management**: Organize reading lists and track progress.
* **Rich Notes**: Write markdown-driven notes.
* **Peer Comments**: Read and comment on collaborative notes.

### 🏗 Core Architecture
It utilizes Clean Architecture, separating database entities, schemas, REST routers, and business logic into isolated layers.
    """,
    version="1.0.0",
    contact={
        "name": "MemoStack API Support",
        "email": "support@memostack.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=openapi_tags,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"{request.client.host} - \"{request.method} {request.url.path}\" "
        f"{response.status_code} - {process_time:.4f}s"
    )
    return response

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root(request: Request):
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
