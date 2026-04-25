from fastapi import FastAPI
import os
import time

app = FastAPI(title="Pushline Test App")

start_time = time.time()


@app.get("/")
def root():
    return {"message": "Hello from Pushline test app!", "version": "1.0.3"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - start_time, 1),
        "environment": os.getenv("APP_ENV", "unknown"),
    }


@app.get("/info")
def info():
    return {
        "app": "pushline-test-fastapi",
        "python_pid": os.getpid(),
        "commit": os.getenv("COMMIT_SHA", "unknown"),
    }
