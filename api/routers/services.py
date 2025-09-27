from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.session import SessionLocal
from api.deps import require_admin
from schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from services import service as service_service
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Public browse
@router.get("/", response_model=List[ServiceResponse])
def list_services(
    db: Session = Depends(get_db),
    q: str | None = Query(None),
    price_min: float | None = Query(None),
    price_max: float | None = Query(None),
    active: bool | None = Query(None)
):
    return service_service.list_services(db, q, price_min, price_max, active)

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    return service_service.get_service(db, service_id)

# Admin endpoints
@router.post("/", response_model=ServiceResponse, status_code=201)
def create_service(
    data: ServiceCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return service_service.create_service(db, data)

@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    data: ServiceUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    return service_service.update_service(db, service_id, data)

@router.delete("/{service_id}", status_code=204)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    service_service.delete_service(db, service_id)
    return None
