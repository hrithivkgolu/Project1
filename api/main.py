from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse

app = FastAPI(title="LLM Code Generation Pipeline API")


async def process_task(data: dict):
    """
    Placeholder for your background processing.
    Example:
    - Call OpenAI API to generate code
    - Push files to GitHub
    - Notify evaluation_url
    """
    print("Processing task in background:", data["task"])
    # Here you would add your LLM + GitHub integration logic
    # For now, just simulate a long-running task
    # e.g., await openai_call(data) or push_to_github(data)
    return True


@app.post("/receive")
async def receive(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="No JSON payload provided.")

        # Validate required fields minimally
        required_fields = ["email", "secret", "task", "round", "brief"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing field: {field}")

        # Start background processing
        # background_tasks.add_task(process_task, data)

        return JSONResponse(
            content={
                "status": "Accepted",
                "message": "Task validated and code generation pipeline has been initiated.",
                "task_id": data.get("task"),
                "round": data.get("round"),
                "nonce": data.get("nonce")
            },
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        # Catch-all error to prevent 500
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/receive")
async def receive_info():
    return {
        "message": "This endpoint requires a POST request with a JSON payload.",
        "schema_required": {
            "email": "string",
            "secret": "string",
            "task": "string",
            "round": "integer",
            "nonce": "string",
            "brief": "string",
            "checks": "list of strings",
            "evaluation_url": "string (URL)",
            "attachments": "list of {name, url} objects"
        }
    }