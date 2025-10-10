"""
Sets up the backend's database and session factory.
Also includes image compression helpers.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base
from env import database_url  # uses the resolved URL from env.py

# --- Engine ---
connect_args = {}
if database_url.startswith("sqlite"):
    # SQLite needs this when used in multi-threaded FastAPI
    connect_args = {"check_same_thread": False}

engine = create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)

# Create all tables once at import (safe if run multiple times)
Base.metadata.create_all(bind=engine)

# --- Session factory ---
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Optional: image compression helpers -----
from PIL import Image
import io
import zlib
import cv2
import numpy as np

def compress_image(image_bytes: bytes, quality: int = 50) -> bytes:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()

def compress_data(data: bytes) -> bytes:
    return zlib.compress(data, level=9)

def decompress_data(compressed_data: bytes) -> bytes:
    return zlib.decompress(compressed_data)

def decompress_image(compressed_image_bytes: bytes):
    image = Image.open(io.BytesIO(compressed_image_bytes)).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
