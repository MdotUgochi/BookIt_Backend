from sqlalchemy.orm import Session
from models.service import Service
from schemas.service import ServiceCreate, ServiceUpdate
from fastapi import HTTPException
from repositories.service import ServiceRepository

def list_services(
    db: Session,
    q: str = None,
    price_min: float = None,
    price_max: float = None,
    active: bool = None
):
    return ServiceRepository.list(db, q, price_min, price_max, active)

def get_service(db: Session, service_id: int) -> Service:
    service = ServiceRepository.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

def create_service(db: Session, payload: ServiceCreate) -> Service:
    service = Service(**payload.dict())
    return ServiceRepository.create(db, service)

def update_service(db: Session, service_id: int, payload: ServiceUpdate) -> Service:
    service = ServiceRepository.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(service, key, value)

    return ServiceRepository.update(db, service)

def delete_service(db: Session, service_id: int):
    service = ServiceRepository.get_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    ServiceRepository.delete(db, service)
    return {"msg": "Service deleted"}
