from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "am i alive"}

@app.post("/receive")
async def receive(request: Request):
    data = await request.json()
    return {"received": data}