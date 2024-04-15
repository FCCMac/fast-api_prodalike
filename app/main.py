from typing import Any, Callable, TypeVar
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

from app.app_config import settings
from app.routers.todos import todos


F = TypeVar("F", bound=Callable[..., Any])

description = """
This example Todo service was built with [FastAPI🚀](https://fastapi.tiangolo.com)

📁 [Source Code](https://github.com/FCCMac/fast-api_prodalike)
🪲 [Report an Issue](https://github.com/FCCMac/fast-api_prodalike/issues)
🧑‍💻 Written by [FCCMac](https://github.com/FCCMac)
"""

app = FastAPI(
    title="FastAPI Todo Web Service",
    description=description,
    version="1.0.0",
    docs_url="/",
    root_path=settings.root_path,
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)


@app.middleware("http")
async def process_time_log_middleware(request: Request, call_next: F) -> Response:
    """
    Add API process time in response headers and log calls
    """

    start_time = time.time()
    response: Response = await call_next(request)
    process_time = str(round(time.time() - start_time, 3))
    response.headers["X-Process-Time"] = process_time

    logger.info(
        f"Method={request.method} Path={request.url.path} StatusCode={response.status_code} ProcessTime={process_time}"
    )

    return response

app.include_router(
    todos.router,
    prefix="/v1/todos",
    tags=["todos"],
)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="error",
        reload=True,
    )
