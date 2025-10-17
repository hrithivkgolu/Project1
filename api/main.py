from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import json
import os
import requests

# NOTE: For deployment on Vercel or other platforms, ensure you have a 'requirements.txt' file
# in your project root containing:
# fastapi
# uvicorn (or equivalent ASGI server)
# requests
# python-multipart (if handling forms, though not used here)

app = FastAPI(title="LLM Task Processor API")

@app.post("/receive")
async def receive_task_endpoint(request: Request):

    aipipe_token = os.environ.get('AIPIPE_TOKEN')
    if not aipipe_token:
        # FastAPI way to handle server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Server configuration error: AIPIPE_TOKEN environment variable is not set.'
        )

    try:
        # 2. Parse the incoming JSON body asynchronously
        request_body = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid JSON format in request body.'
        )

    task_description = request_body.get('brief')
    specific_model = request_body.get('specificModel', 'gpt-4o')

    if not task_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Missing required field: "taskDescription" in the request body.'
        )

    try:
        AI_SYSTEM_PROMPT = "You are an expert AI task execution agent. Your role is to carefully analyze the user's request and provide a clear, detailed, and actionable response that fully completes the task."

        payload = {
            'model': specific_model,
            'messages': [
                {'role': 'system', 'content': AI_SYSTEM_PROMPT},
                {'role': 'user', 'content': task_description}
            ],
            'temperature': 0.7,
            'max_tokens': 2048
        }
        AIPIPE_ENDPOINT = 'https://aipipe.org/openai/v1/chat/completions'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {aipipe_token}'
        }

        api_response = requests.post(AIPIPE_ENDPOINT, headers=headers, json=payload, timeout=60)
        api_data = api_response.json()

        # 5. Handle API response
        if not api_response.ok:
            print(f'AI Pipe API Error: {api_data}')
            error_details = api_data.get('error', {}).get('message', 'Unknown AI Pipe error')
            
            # Use upstream status code if available, otherwise default to 500
            error_status_code = api_response.status_code if api_response.status_code >= 400 else status.HTTP_500_INTERNAL_SERVER_ERROR

            raise HTTPException(
                status_code=error_status_code,
                detail={
                    'error': 'Failed to complete AI task.',
                    'details': error_details
                }
            )

        # 6. Extract the generated text and return to the client
        generated_text = api_data.get('choices', [{}])[0].get('message', {}).get('content', 'Error: No content generated.')

        return JSONResponse(
            content={
                'taskExecuted': True,
                'model': api_data.get('model'),
                'result': generated_text,
                'usage': api_data.get('usage')
            },
            status_code=status.HTTP_200_OK
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f'Server Function Execution Error: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Internal Server Error during task processing: {str(e)}'
        )

@app.get("/")
async def root():
    return {
        "service": "LLM Task Processor API",
        "status": "OK",
        "endpoint": "/receive (POST)"
    }