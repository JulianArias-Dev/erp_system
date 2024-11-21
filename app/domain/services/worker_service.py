from app.persistance.repository import worker_repository

def create_worker(db, worker_data):
    return worker_repository.create_worker(db, worker_data)

def get_all_workers(db):
    return worker_repository.get_all_workers(db)

def get_worker_by_uid(db, uid):
    return worker_repository.get_worker_by_uid(db, uid)

def update_worker(db, worker_id, update_data):
    return worker_repository.update_worker(db, worker_id, update_data)

def delete_worker(db, worker_id):
    return worker_repository.delete_worker(db, worker_id)
