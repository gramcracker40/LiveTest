'''
Main configuration file for the backend application 
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.scantron import router as scantron_router
from routers.users import router as user_router
from routers.test import router as test_router
from routers.course import router as course_router

app = FastAPI(
    title="LiveTest",
    description="backend for test scanning app",
    version="0.0.1",
    contact={
        "name": "Garrett Mathers",
        "url": "https://github.com/gramcracker40",
        "email": "garrett.mathers@gmail.com",
    },)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(course_router)
app.include_router(test_router)
app.include_router(scantron_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
