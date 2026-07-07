from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import uuid

app = FastAPI()

EMAIL = "23f2001401@ds.study.iitm.ac.in"

START_TIME = time.time()

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

logs = []


@app.middleware("http")
async def log_requests(request: Request, call_next):
    REQUEST_COUNTER.inc()

    request_id = str(uuid.uuid4())

    logs.append({
        "level": "INFO",
        "ts": time.time(),
        "path": request.url.path,
        "request_id": request_id
    })

    if len(logs) > 1000:
        logs.pop(0)

    response = await call_next(request)
    return response


@app.get("/work")
def work(n: int = 1):
    for _ in range(n):
        pass
    return {
        "email": EMAIL,
        "done": n
    }


@app.get("/healthz")
def health():
    return {
        "status": "ok",
        "uptime_s": time.time() - START_TIME
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/logs/tail")
def tail(limit: int = 10):
    return logs[-limit:]