from fastapi import FastAPI, Request

app = FastAPI(title="Smart Food Assistant")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/workflows/test")
async def workflow_test(request: Request):
    payload = await request.json()
    return {"received": payload}