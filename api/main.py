from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
#from pipeline_worker.seerun import run_pipeline, EvaluationRequest

app = FastAPI(title="LLM Code Generation Pipeline API")


@app.get("/")
async def root():
    return {
        "service": "LLM Code Generation Pipeline API",
        "status": "OK",
        "version": "1.0.0"
    }


@app.post("/receive")
async def receive(data: EvaluationRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_pipeline, data.model_dump())
    return JSONResponse(
        content={
            "status": "Accepted",
            "message": "Task validated and code generation pipeline has been initiated.",
            "task_id": data.task,
            "round": data.round
        }, 
        status_code=status.HTTP_202_ACCEPTED
    )

@app.get("/receive")
async def receive_info():
    return {
        "message": "This endpoint requires a POST request with a JSON payload.",
        "schema_required": "Please provide a JSON object matching the EvaluationRequest structure."
    }
