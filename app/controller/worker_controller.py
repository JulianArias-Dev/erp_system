from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config import get_db
from app.domain.services import worker_service
from app.domain.schemas.worker_shema import WorkerCreate, WorkerUpdate, WorkerResponse

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("/", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    return worker_service.create_worker(db, worker.dict())

@router.get("/", response_model=list[WorkerResponse])
def list_workers(db: Session = Depends(get_db)):
    return worker_service.get_all_workers(db)

@router.get("/{uid}", response_model=WorkerResponse)
def get_worker(uid: str, db: Session = Depends(get_db)):
    worker = worker_service.get_worker_by_uid(db, uid)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    return worker

@router.put("/{worker_id}", response_model=WorkerResponse)
def update_worker(worker_id: int, worker: WorkerUpdate, db: Session = Depends(get_db)):
    updated_worker = worker_service.update_worker(db, worker_id, worker.dict(exclude_unset=True))
    if not updated_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    return updated_worker

@router.delete("/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = worker_service.delete_worker(db, worker_id)
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
