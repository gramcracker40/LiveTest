'''
Sets up the backends database
also initializes the 'session maker' that allows for 
sessions to be initiated with the db and query it.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env import database_url
from tables import Base
from PIL import Image
import io
import zlib
import cv2
import numpy as np

engine = create_engine(database_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# helper to get a database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# helper functions for image compression/decompression in database
def compress_image(image_bytes, quality=50):
    image = Image.open(io.BytesIO(image_bytes))
    compressed_image_io = io.BytesIO()
    image.save(compressed_image_io, format="JPEG", quality=quality)
    compressed_image_bytes = compressed_image_io.getvalue()
    return compressed_image_bytes

def compress_data(data):
    compressed_data = zlib.compress(data, level=9)
    return compressed_data


def decompress_data(compressed_data):
    return zlib.decompress(compressed_data)

def decompress_image(compressed_image_bytes):
    image = Image.open(io.BytesIO(compressed_image_bytes))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)