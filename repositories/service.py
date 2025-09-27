from sqlalchemy.orm import Session
from models.service import Service

class ServiceRepository:

    @staticmethod
    def get_by_id(db: Session, service_id: int) -> Service | None:
        return db.query(Service).filter(Service.id == service_id).first()

    @staticmethod
    def get_active_by_id(db: Session, service_id: int) -> Service | None:
        return db.query(Service).filter(
            Service.id == service_id,
            Service.is_active == True
        ).first()

    @staticmethod
    def list(
        db: Session,
        q: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        active: bool | None = None,
    ):
        query = db.query(Service)
        if q:
            query = query.filter(Service.title.ilike(f"%{q}%"))
        if price_min is not None:
            query = query.filter(Service.price >= price_min)
        if price_max is not None:
            query = query.filter(Service.price <= price_max)
        if active is not None:
            query = query.filter(Service.is_active == active)
        return query.all()

    @staticmethod
    def create(db: Session, service: Service) -> Service:
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def update(db: Session, service: Service) -> Service:
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete(db: Session, service: Service):
        db.delete(service)
        db.commit()
