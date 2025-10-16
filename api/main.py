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

@app.post("/receive")
async def receive(request: Request):
    data = await request.json()
    return {"received": data}


@app.post("/receive")
async def receive(data: TaskData):

    print("--- New Evaluation Request Received ---")
    print(f"Task ID: {request_data.task} | Round: {request_data.round}")
    print(f"Student Email: {request_data.email}")
    print(f"Brief: {request_data.brief[:80]}...")
    print(f"Evaluation URL: {request_data.evaluation_url}")
    print(f"Attachments Count: {len(request_data.attachments)}")
    
    return JSONResponse(
        status_code=202,
        content={
            "status": "Accepted",
            "task_key": f"{request_data.task}-{request_data.round}",
            "message": "Task validated and asynchronous code generation pipeline initiated."
        }
    )