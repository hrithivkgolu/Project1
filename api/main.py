from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pipeline_worker.seerun import run_pipeline

app = FastAPI()

@app.get("/")
async def root():
    return {
        run_pipeline()
        "service": "LLM Code Generation Pipeline API",
        "status": "OK",
        "version": "1.0.0"
    }


@app.post("/receive")
async def receive_json(request: Request):
    try:
        data = await request.json() 
        return JSONResponse(content= "HTTP 200", status_code=200)
    except Exception:
        return JSONResponse(content={"message": "No data available"}, status_code=400)

@app.get("/receive")
async def receive():
    return {
        "use post to give json file"
    }





