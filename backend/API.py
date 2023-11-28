'''
Main configuration file for the fastapi backend application 
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, course_router,\
        test_router, scantron_router, auth_router

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
app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
