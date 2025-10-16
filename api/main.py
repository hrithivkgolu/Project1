from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {
        "service": "LLM Code Generation Pipeline API",
        "status": "OK",
        "version": "1.0.0"
    }



