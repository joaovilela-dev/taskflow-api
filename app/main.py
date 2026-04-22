from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.database.connection import create_tables
from app.routes import user_routes, task_routes, category_routes

setup_logging()
logger = logging.getLogger(settings.APP_NAME)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
## 🚀 TaskFlow API

API REST completa para gerenciamento de tarefas com autenticação JWT.

### Funcionalidades
- 🔐 **Autenticação** via JWT (registro e login)
- 📋 **Tarefas** com CRUD completo, filtros e paginação
- 🗂️ **Categorias** personalizadas por usuário
- ✅ **Status**: pending → in_progress → done
- 🔥 **Prioridades**: low, medium, high
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware de tempo de resposta ───────────────────────────────────────────
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{duration:.2f}ms"
    logger.info(f"{request.method} {request.url.path} → {response.status_code} ({duration:.1f}ms)")
    return response


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION} iniciando...")
    create_tables()
    logger.info("✅ Banco de dados pronto")


# ── Rotas ─────────────────────────────────────────────────────────────────────
app.include_router(user_routes.router)
app.include_router(task_routes.router)
app.include_router(category_routes.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["⚡ Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["⚡ Health"])
def health():
    return {"status": "healthy"}