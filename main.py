from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:postgres@db:5432/appdb"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)
app = FastAPI()

class PatientIn(BaseModel):
    name: str
    age: int

@app.get("/patients")
def list_patients():
    s = Session()
    rows = s.query(Patient).all()
    return [{"id": r.id, "name": r.name, "age": r.age} for r in rows]

@app.post("/patients")
def create_patient(p: PatientIn):
    s = Session()
    new = Patient(name=p.name, age=p.age)
    s.add(new); s.commit(); s.refresh(new)
    return {"id": new.id, "name": new.name, "age": new.age}
