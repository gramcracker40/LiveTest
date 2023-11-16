from fastapi import FastAPI
app = FastAPI()

from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from Models import Scantron
from Database import session

class ScantronCreate(BaseModel):
    scantron_photo: bytes
    student_id: int
    test_id: int
    
class Scantron(BaseModel):
    num_questions: int
    answers: str
    grade: float
    student_id: int
    test_id: int


@app.post("/scantrons/", response_model=Scantron)
def create_scantron(scantron: ScantronCreate):
    db_scantron = Scantron(**scantron.__dict__)
    session.add(db_scantron)
    session.commit()
    
    return db_scantron

@app.get("/scantrons/{scantron_id}", response_model=Scantron)
def read_scantron(scantron_id: int):
    db = session()
    db_scantron = db.query(Scantron).filter(Scantron.id == scantron_id).first()
    db.close()
    if db_scantron is None:
        raise HTTPException(status_code=404, detail="Scantron not found")
    return db_scantron

@app.put("/scantrons/{scantron_id}", response_model=Scantron)
def update_scantron(scantron_id: int, scantron: ScantronCreate):
    db = session()
    db_scantron = db.query(Scantron).filter(Scantron.id == scantron_id).first()
    if db_scantron is None:
        db.close()
        raise HTTPException(status_code=404, detail="Scantron not found")
    for key, value in scantron.dict().items():
        setattr(db_scantron, key, value)
    db.commit()
    db.refresh(db_scantron)
    db.close()
    return db_scantron

@app.delete("/scantrons/{scantron_id}", response_model=Scantron)
def delete_scantron(scantron_id: int):
    db = session()
    db_scantron = db.query(Scantron).filter(Scantron.id == scantron_id).first()
    if db_scantron is None:
        db.close()
        raise HTTPException(status_code=404, detail="Scantron not found")
    db.delete(db_scantron)
    db.commit()
    db.close()
    return db_scantron

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
