from fastapi import FastAPI
from backend.routers import scantron

app = FastAPI()

app.include_router(scantron.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
