from fastapi import FastAPI
from routers.scantron import router as scantron_router
from routers.users import router as user_router

app = FastAPI()

app.include_router(scantron_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
