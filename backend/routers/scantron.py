from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from tables import Scantron
from db import session
from models.scantron import Scantron, ScantronCreate

router = APIRouter(
    prefix="/scantron",
    tags=["scantron"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Scantron)
def create_scantron(scantron: ScantronCreate):
    db_scantron = Scantron(**scantron.__dict__)
    session.add(db_scantron)
    session.commit()
    
    return db_scantron

@router.get("/{scantron_id}", response_model=Scantron)
def read_scantron(scantron_id: int):
    db = session()
    db_scantron = db.query(Scantron).filter(Scantron.id == scantron_id).first()
    db.close()
    if db_scantron is None:
        raise HTTPException(status_code=404, detail="Scantron not found")
    return db_scantron

@router.put("/{scantron_id}", response_model=Scantron)
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

@router.delete("/{scantron_id}", response_model=Scantron)
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