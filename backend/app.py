import argparse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router, course_router, test_router, \
            submission_router, auth_router, enrollment_router

def get_api() -> FastAPI:
    '''
    Builds the backend of test scanning app
    factory pattern
    '''
    app = FastAPI(
        title="LiveTest",
        description="backend for test scanning app",
        version="1.1",
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
        allow_headers=["*"]
    )

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(course_router)
    app.include_router(enrollment_router)
    app.include_router(test_router)
    app.include_router(submission_router)

    return app

app = get_api()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the FastAPI app with optional port and reload arguments.')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the application on')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for the application')
    
    args = parser.parse_args()

    uvicorn.run("app:app", host="0.0.0.0", port=args.port, reload=args.reload)
