import argparse
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from routers import user_router, course_router, test_router, submission_router, auth_router, enrollment_router

# NEW: pull in DB + models + env (loads .env already)
from db import engine, SessionLocal
from tables import Base, Teacher
from env import admin_user, admin_pass  # reads ADMIN_USER / ADMIN_PASS

def get_api() -> FastAPI:
    """
    Builds the backend of test scanning app
    factory pattern
    """
    app = FastAPI(
        title="LiveTest",
        description="backend app for LiveTest",
        version="1.1",
        contact={
            "name": "Garrett Mathers",
            "url": "https://github.com/gramcracker40",
            "email": "garrett.mathers@gmail.com",
        },
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(course_router)
    app.include_router(enrollment_router)
    app.include_router(test_router)
    app.include_router(submission_router)

    @app.on_event("startup")
    def _seed_admin():
        # Ensure tables are present (safe to call again)
        Base.metadata.create_all(bind=engine)

        if not admin_user or not admin_pass:
            # Nothing to seed if not configured
            return

        # Normalize admin email if a bare username was provided
        email = admin_user if "@" in admin_user else f"{admin_user}@local"
        name = "Admin" if admin_user.lower() == "admin" else admin_user

        db: Session = SessionLocal()
        try:
            row = db.query(Teacher).filter(Teacher.email == email).one_or_none()
            if row:
                # keep this simple since current model stores plaintext
                if row.password != admin_pass or row.name != name:
                    row.password = admin_pass
                    row.name = name
                    db.add(row)
                    db.commit()
            else:
                db.add(Teacher(name=name, email=email, password=admin_pass))
                db.commit()
        except IntegrityError:
            db.rollback()
        finally:
            db.close()

    return app

app = get_api()

if __name__ == "__main__":
    import uvicorn
    parser = argparse.ArgumentParser(description="Run the FastAPI app with optional port and reload arguments.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the application on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for the application")
    args = parser.parse_args()

    uvicorn.run("app:app", host="0.0.0.0", port=args.port, reload=args.reload)
