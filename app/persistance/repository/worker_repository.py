from sqlalchemy.orm import Session
from app.persistance.models.worker_model import Worker

def create_worker(db: Session, worker_data):
    worker = Worker(**worker_data)
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

def get_all_workers(db: Session):
    return db.query(Worker).all()

def get_worker_by_uid(db: Session, uid: str):
    return db.query(Worker).filter(Worker.uid == uid).first()

def update_worker(db: Session, worker_id: int, update_data: dict):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        return None
    for key, value in update_data.items():
        setattr(worker, key, value)
    db.commit()
    db.refresh(worker)
    return worker

def delete_worker(db: Session, worker_id: int):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker:
        db.delete(worker)
        db.commit()
    return worker
