from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Models import Teacher
from Database import session

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# Define API routes for the Teacher resource
@app.post("/teachers/")
def create_teacher(teacher: Teacher, db: Session = Depends(get_db)):
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@app.get("/teachers/")
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return teachers

@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, updated_teacher: Teacher, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in updated_teacher.dict().items():
        setattr(teacher, key, value)
    db.commit()
    db.refresh(teacher)
    return teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}
