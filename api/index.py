from main import app
from fastapi.responses import PlainTextResponse

# For vercel-python serverless runtime
def handler(request, context):
    return PlainTextResponse("Use /api for FastAPI routes")

# Export FastAPI app
app = app